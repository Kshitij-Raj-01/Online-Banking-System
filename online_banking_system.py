import pickle
import os
import pathlib
from twilio.rest import Client

Admin="Admin12345" #Admin Password

class Account :
    accNo = 0
    name = ""
    deposit=0
    type = ""
    def createAccount(self):
        self.accNo= int(input("Enter the account no : "))
        self.password=input("Create a password : ")
        self.name = input("Enter the account holder name : ")
        self.mob=input("Enter your phone Number : ")
        self.type = input("Enter the type of account [C/S] : ")
        self.deposit = int(input("Enter The Initial amount(>=500 for Saving and >=1000 for current : "))
        sms(self.accNo,1,self.name,self.mob)
        print("\n\n\nAccount Created")
    def showAccount(self):
        print("Account Number : ",self.accNo)
        print('Account Password : ',self.password)
        print("Account Holder Name : ", self.name)
        print("Mobile : ",self.mob)
        print("Type of Account",self.type)
        print("Balance : ",self.deposit)
    def modifyAccount(self):
        print("Account Number : ",self.accNo)
        self.name = input("Modify Account Holder Name :")
        self.type = input("Modify type of Account :")
        self.deposit = int(input("Modify Balance :"))
    def depositAmount(self,amount):
        self.deposit += amount  
    def withdrawAmount(self,amount):
        self.deposit -= amount  
    def report(self):
        print(self.accNo," ",self.password, " ",self.name ," ",self.type," ", self.deposit)  
    def getAccountNo(self):
        return self.accNo
    def getPassword(self):
        return self.password
    def getAcccountHolderName(self):
        return self.name
    def getMobile(self):
        return self.mob
    def getAccountType(self):
        return self.type
    def getDeposit(self):
        return self.deposit
    
def intro():

   print("\t\t\t\t**********************")

   print('\t\t\t\t  Welcome to R&K BANK')

   print('\t\t\t\t**********************')

   print('\t\t\t\tBrought To You By:')

   print('\t\t\t\tRavi Raushan and Kshtij Raj')

def writeAccount():
    account=Account()
    account.createAccount()
    createAccountFile(account)

def createAccountFile(account):
    file=pathlib.Path("accounts.data")
    if file.exists():
        inFile=open('accounts.data','rb')
        outFile=pickle.load(inFile)
        outFile.append(account)
        inFile.close()
        os.remove("accounts.data")
        inFile=open('accounts.data','wb')
        pickle.dump(outFile,inFile)
        inFile.close()
    else:
        oldlist = [account]
        outFile = open("accounts.data","wb")
        pickle.dump(oldlist, outFile)
        outFile.close()
        os.rename("accounts.data", "accounts.data")  

def checkPassword(pword):
    file=pathlib.Path("accounts.data")
    if file.exists ():
        infile = open('accounts.data','rb')
        mylist = pickle.load(infile)
        infile.close()
        allow=False
        for item in mylist :
            if item.password==pword:
                allow=True
                return allow
    else:
        print("No data found\n")

def depositAndWithdraw(num1, num2):
    file=pathlib.Path("accounts.data")
    if file.exists ():
        infile = open('accounts.data','rb')
        mylist = pickle.load(infile)
        infile.close()
        for item in mylist :
            if item.accNo==num1:
                if num2 == 1 :
                    os.remove("accounts.data")
                    amount = int(input("Enter the amount to deposit : "))
                    item.deposit+=amount 
                    outfile = open("accounts.data","wb")
                    pickle.dump(mylist, outfile)
                    outfile.close()
                    os.rename("accounts.data", "accounts.data")
                    print("Your account is updted\n")
                    break
                elif num2 == 2 :
                    amount = int(input("Enter the amount to withdraw : "))
                    if amount <= item.deposit :
                        os.remove("accounts.data")
                        item.deposit -=amount
                        outfile = open("accounts.data","wb")
                        pickle.dump(mylist, outfile)
                        outfile.close()
                        os.rename("accounts.data", "accounts.data")
                        print("Your account is updted\n")
                        break
                    else :
                        print("You cannot withdraw larger amount\n")

            

def displayBalance(num):
    file=pathlib.Path("accounts.data")
    if file.exists():
        inFile=open('accounts.data','rb')
        mylist=pickle.load(inFile)
        inFile.close()
        found = False
        for item in mylist :
            if item.accNo == num :
                print("Your account Balance is = ",item.deposit,"\n")
                found = True
                break
        if not found :
            print("No existing record with this number\n")

def displayAll():
    file = pathlib.Path("accounts.data")
    if file.exists ():
        infile = open("accounts.data",'rb')
        mylist = pickle.load(infile)
        for item in mylist :
            print(item.accNo," ",item.password," ", item.name, " ",item.type, " ",item.deposit )
            infile.close()
    else :
        print("No records to display\n")            

def deleteAccount(num):
    file = pathlib.Path("accounts.data")
    if file.exists ():
        infile = open("accounts.data","rb")
        oldlist = pickle.load(infile)
        infile.close()
        newlist = []
        for item in oldlist :
            if item.accNo != num :
                newlist.append(item)
            else:
                sms(num,6,item.name,item.mob)
        os.remove("accounts.data")
        outfile = open("accounts.data","wb")
        pickle.dump(newlist, outfile)
        outfile.close()
        os.rename("accounts.data", "accounts.data")
        print("Your account is closed\n")

def modifyAccount(num):
    file = pathlib.Path("accounts.data")
    if file.exists ():
        infile = open("accounts.data","rb")
        oldlist = pickle.load(infile)
        infile.close()
        os.remove("accounts.data")
        for item in oldlist :
            if item.accNo == num :
                item.name = input("Enter the account holder name : ")
                item.password=input("Create new password : ")
                item.type = input("Enter the account Type : ")
                item.mob=int(input("Enter the mobile number : "))
                sms(num,7,item.name,item.mob)     
        outfile = open("accounts.data","wb")
        pickle.dump(oldlist, outfile)
        outfile.close()
        os.rename("accounts.data", "accounts.data")
        print("Data Updated\n")

def sms(acc,opt,name,mob):
    account_sid="api key" #Enter your api
    auth_token='auth_token' #Enter your key
    my_phone_number='[+country code][phone number]' #Enter your registered phone Number
    
    client=Client(account_sid, auth_token)
    if opt==1:
        message=client.messages.create(
            body=f'''\nNew Account created
        User Name : {name}
        Account Number : {acc}
        Mobile Number : {mob}''',
            from_='given phone number', #Enter your given phone number
            to=my_phone_number
        )
        print(message.body)
        os.system('cls')
    elif opt==6:
        message=client.messages.create(
            body=f'''\nAccount Closed
        Account Number : {acc}
        User Name : {name}
        Mobile Number : {mob}''',
            from_='given phone number',  #Enter your given phone number
            to=my_phone_number
        )
        print(message.body)
        os.system('cls')
    elif opt==7:
        message=client.messages.create(
            body=f'''\nAccount Updated
        Account Number : {acc}
        User Name : {name}
        Mobile Number : {mob}''',
            from_='given phone number',  #Enter your given phone number
            to=my_phone_number
        )
        print(message.body)
        os.system('cls')

ch=""
num=0
intro()
while ch != 8:
   print("\tMAIN MENU")
   print("\t1. NEW ACCOUNT")
   print("\t2. DEPOSIT AMOUNT")
   print("\t3. WITHDRAW AMOUNT")
   print("\t4. BALANCE ENQUIRY")
   print("\t5. ALL ACCOUNT HOLDER LIST")
   print("\t6. CLOSE AN ACCOUNT")
   print("\t7. MODIFY AN ACCOUNT")
   print("\t8. EXIT")
   print("\tSelect Your Option (1-8) ")
   ch = input()
   os.system("cls");  
   if ch == "1":
       writeAccount()
   elif ch =="2":
        num = int(input("\tEnter The account No. : "))
        pword=input("Enter your password : ")
        allow=checkPassword(pword)
        if allow==True:
            depositAndWithdraw(num, 1)
        else:
            print("Invalid Password\n")
   elif ch == "3":
        num = int(input("\tEnter The account No. : "))
        pword=input("Enter your password : ")
        allow=checkPassword(pword)
        if allow==True:
            depositAndWithdraw(num, 2)
        else:
            print("Invalid Password\n")
   elif ch == "4":
        num = int(input("\tEnter The account No. : "))
        pword=input("Enter your password : ")
        allow=checkPassword(pword)
        if allow==True:
            displayBalance(num)
        else:
            print("Invalid Password\n")
   elif ch == "5":
        pword=input("Enter Admin password : ")
        if pword==Admin:
            displayAll()
        else:
            print("Invalid Password\n")
   elif ch == "6":
        num =int(input("\tEnter The account No. : "))
        pword=input("Enter your password : ")
        allow=checkPassword(pword)
        if allow==True:
            deleteAccount(num)
        else:
            print("Invalid Password\n")
   elif ch == "7":
        num = int(input("\tEnter The account No. : "))
        pword=input("Enter your password : ")
        allow=checkPassword(pword)
        if allow==True:
            modifyAccount(num)
        else:
            print("Invalid Password\n")
   elif ch == "8":
       print("\tThanks for using bank management system\n")
       break
   else :
       print("Invalid choice\n")