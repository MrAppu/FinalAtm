from sys import time,exit
import secrets
import hashlib
import pickle
from os import path
import getpass

#===================================== LOGIN INTERFACE =====================================#

def first_input():
    '''This prints out the the main menu to navigate to other menus'''
    print('''
    ###############################
    ##### Welcome to the ATM! #####
    ###############################
    
       Please select your option:
       1. Login into the system
       2. Create a new account
       3. Exit''')   
    run_inp=input('Enter the option you need:')
    if  run_inp=='1':
        Login_Card()
    elif run_inp=='2':
        Login_Name()
    elif run_inp=='3':
        print('Thank you for coming. Visit again!. Press "Enter" to exit')
        input()
        exit("Bye! Have a great day!")   #If you want to change it, use "first_input()"
    elif run_inp=='adminconsole':
        print('Initialising admin console')       
    else:
        print("Please enter the correct number.  Press 'Enter' key to restart")
        input()
        first_input()

def Login_Name():
    get_user=input("Enter your username. Type '0' to go back:")
    if get_user.isalnum()==True:
        if get_user=='0':
            print("First input")
        if len(get_user)>=64:
            print("All usernames must be below 64 charectors")
            input()
            Login_Name()
        else:
            Login_Pin(get_user,'sign.up')
    else:
        print("Only alpha-numeric charectors allowed. Press 'Enter' to go back")
        input()
        Login_Name()  

def Login_Card():
    while True:
        try:
            global card
            card=int(input("Enter your 12 digit Card Number. Type '0' to go back:"))
            if card==0:
                first_input()
            elif len(str(card))==12:
                access(card=card,other='check')     
            else:
                print("Please enter 12 digits. Press 'Enter' key to restart")
                input()
                Login_Card()
        except ValueError:
          print("Please use numbers. Press Enter key to restart")
          input()
          Login_Card()

def Login_Pin(username,action):
    pin=getpass.getpass("Enter your 4 digit PIN code.(The password may not be echoed) Type '0' to go back:")
    if pin=='0':
        if action=='sign.up':
            Login_Name()
        if action=='log.in':
            Login_Card()
    elif len(pin)==4:
        if action=='sign.up':
            conf_module(username,pin)
        if action=='log.in':
            print("Please wait a few seconds...")
            time.sleep(3)
            access(card=username,pinp=pin,other='login')
    else:
        print("Please enter 4 digits. Press 'Enter' key to restart")
        input()
        exit("Bye! Have a great day!") #If you want to continue, user Login_Pin(username,action) 

def conf_module(user,pin):
    print(f'''Confirm your Username and PIN
    Username : {user}
    PIN : {pin}
    ''')
    conf=input("Confirmation required Y/N: ").lower()
    if conf == 'y':
        card_num(user,pin)  
    elif conf == 'n':
        sconf()
    else:
        print('Please enter Y/N. Press enter to go back ')
        input()
        conf_module(user,pin)
def sconf():
    sec_conf=input("Would you like to try it again? Y/N").lower()    
    if sec_conf == 'y':
        Login_Name()
    elif sec_conf == 'n':
        print("Exiting now!")
        print("Thank you for using the ATM, visit again!!")
        first_input() 


#====================================== CARD MODULES =======================================# 
        
def card_num(usr,pin):
        card_gen()
        card_checker(str(crdnum))
        print('This is your card number. Keep it safe') 
        splitting_card(crdnum) 
        print('Please Wait')
        crypt(usr,pin,crdnum)
        print("You have sucessfully registered. Press Enter to go back")
        input()
        first_input() 

def card_gen():
    '''This module generates a random secure number of 12 digits.'''
    global crdnum
    crdnum=secrets.randbelow(int(1e12))
    if len(str(crdnum))==12:
        pass
    else:
        card_gen()               
def card_checker(string):     
    with open(GetFileLoc("card.txt"), "a+") as file:
        for line in file:
            line = line.rstrip()
            if string in line:
                if string==line:
                    card_num()
        else:
            file.write(string+'\n')
def splitting_card(s):
    s=str(s)
    a=(s[:4])
    b=(s[4:8])
    c=(s[8:12])
    print(a+' '+b+' '+c)            


#================================= CRYPTOGRAPHIC FUNCTIONS ==================================#

def crypt(user,pin,card):
    pwd=bytes(user+str(pin)+str(card), encoding='utf8')
    mix_salt=secrets.token_bytes(32)
    key=hashlib.scrypt(password=pwd, salt=mix_salt, n=16384, r=8, p=1, dklen=64)
    users={}
    users[f"{user}",f"{card}"] = {
        "salt": mix_salt,
        "key" : key
    }
    with open(GetFileLoc('login.atm'),'ab') as data:    
        pickle.dump(users,data)

def check_pwd(card,user,pin):
    tup = (user,card)
    up_user=up[tup]
    get_salt=(up_user.get('salt', 'A fatal error has occured. Inform the admin and give this error: "0xs0"'))
    get_key=(up_user.get('key', 'A fatal error has occured. Inform the admin and give this error: "0xk0'))
    pwd_check=bytes(user+str(pin)+str(card), encoding='utf8')
    check_key=hashlib.scrypt(password=pwd_check, salt=get_salt, n=16384, r=8, p=1, dklen=64)
    global checking
    if get_key == check_key:
        return True
    else:
        print("Your pin or card number is wrong. Please start from the beginning. Press enter to go back.")
        input()
        Login_Card() 


#===================================== FILE FUNCTIONS =======================================# 

def GetFileLoc(file):
    file_path = path.abspath(__file__)                  # full path of your script
    dir_path = path.dirname(file_path)                  # full path of the directory of your script
    file_path = path.join(dir_path, file)
    return file_path     

def access(card,user,pinp,other):  
    with open(GetFileLoc('login.atm'),'rb') as data:    
        global up
        unpickled = []
        while True:
            try:
                unpickled.append(pickle.load(data))
                up=unpickled[-1]
                for i in up:
                    if i[-1]==card:
                        if other=='check':
                            Login_Pin(card,'log.in')
                        if other=='login':
                            if check_pwd(card,user,pinp)==True:
                                print(f'Welcome {user}!')
                            else:
                                print("The card number/password is wrong. Please try again.") 
                                Login_Card()                                                          
                                
                        else:
                            print("The card number/password is wrong. Please try again.") 
                            Login_Card()                                                          
            except EOFError:
                Login_Pin(card,'sign.up')


 


                   



                
