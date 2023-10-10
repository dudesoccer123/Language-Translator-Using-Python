# import all required modules 
import mysql.connector # used to manage tables and queries in sql
from tkinter import * # used to create user interface
import googletrans
from gtts import gTTS
import os # used to manage deletion of files
from playsound import playsound
from googletrans import Translator ,constants
from google_trans_new import google_translator
from tkinter import messagebox # used to diaplay error,info messages
import time # to reord current time for history in csv file
import csv # edit the csv file
from datetime import date # record current date in csv file

    
# Create txt file that consists of supported languages
dval1 = googletrans.LANGUAGES.values()
dval1_list = []
fcreate = open("supported_languages.txt","w")
for i in dval1:
    dval1_list.append(i+'\n')
fcreate.writelines(dval1_list)
fcreate.close()

# Connect to database
mc = mysql.connector.connect(host = 'localhost',user = 'root',database = 'comp_project',password = 'your database password')
cursor = mc.cursor()

# Create table
def crtable():
    cursor.execute('''select count(*) from information_schema.tables
    where table_schema = 'comp_project';''')
    data1 = cursor.fetchall()
    if data1 != [(2,)]:
        cursor.execute("create table userdetails (username char(30) primary key,password varchar(10));")
        cursor.execute("create table reportdetails (username char(30),reported_issue varchar(100) primary key,comments varchar(100));")

crtable()

# Update usernames List
b=[]
cursor.execute('select username from userdetails;')
d = cursor.fetchall()

for i in range (0,len(d)):
    for j in d[i]:
        b.append(j)
        
def RefreshUserList():
    cursor.execute('select username from userdetails;')
    d = cursor.fetchall()

    for i in range (0,len(d)):
        for j in d[i]:
            b.append(j)   
   
RefreshUserList()   

def chpass(uname):

    cursor.execute("select password from userdetails where username = '%s'" %(uname))

    data = cursor.fetchall()

    v =[]
    for row in data:
        for col_value in row:
            v.append(col_value)
    return v

def openfile(x):
    os.system("notepad.exe " + x)

# root variables (main window)
root = Tk()
root.title("LANGTRANS")
root.geometry('750x500')
root.resizable(False, False) 

translator = google_translator()
invert = {v: k for k, v in googletrans.LANGUAGES.items()}
dval = googletrans.LANGUAGES.values()
dval_list = list(dval)



# define all related functions


def logout():   # used to logout of the program
    f2.tkraise()
    usernameentry.delete(0,END)
    passwordentry.delete(0,END)
    cleartext()

def submit():
    RefreshUserList()
    username = usernameentry1.get()
    if username not in b and username != '':
        password = passwordentry1.get()
        conpassword = confirmpasswordentry.get()
        if password == conpassword and password != '' and conpassword != '':
            add_user = ('''insert into userdetails
            values (%s, %s);''')
            data_user = (username,password)
            cursor.execute(add_user,data_user)
            mc.commit()
            print('User created')
            messagebox.showinfo("","User successfully created")
            RefreshUserList()


            ##   create a CSV file for that particular user with that username
            file = open("{}.csv".format(username),'w',encoding='utf-8')
            tempwriter = csv.writer(file)
            tempwriter.writerow(["Translation History data : "])
            tempwriter.writerow(['Date','Time','Original Text','Language','Translated Text'])
            file.close()


            f2.tkraise()
            usernameentry1.delete(0,END)
            passwordentry1.delete(0,END)
            confirmpasswordentry.delete(0,END)
        elif password == '':
            print('Please enter the password')
            messagebox.showinfo("","Please enter the password")
            confirmpasswordentry.delete(0,END)
        elif conpassword == '':
            print('Please confirm the password')
            messagebox.showinfo("","Please confirm the password")
        else:
            print("Password doesnt match")
            messagebox.showinfo("","Password does not match")
            passwordentry1.delete(0,END)
            confirmpasswordentry.delete(0,END)
    elif username == '':
        print('Please enter the username')
        messagebox.showwarning("ERROR","Please enter the username")
        usernameentry1.delete(0,END)
        passwordentry1.delete(0,END)
        confirmpasswordentry.delete(0,END)
    else:
        print("Username already taken")
        messagebox.showinfo("","Selected username is already taken")
        usernameentry1.delete(0,END)
        passwordentry1.delete(0,END)
        confirmpasswordentry.delete(0,END)

def login(): # used to log in user into the program       
    userentry = usernameentry.get()
    passentry = passwordentry.get()
    global n
    global w
    global maindata
    n = userentry
    w = passentry
    if userentry in b:
        v = chpass(userentry)
        if passentry in v:
            maindata = []
            f1.tkraise()
            try :
                translation_text_label.destroy()
                tranentry.delete(0,END)
                language.delete(0,END)
            except:
                pass

        else:
            print("Your username or password is wrong")
            messagebox.showwarning("ERROR","Your username or password is wrong")
            usernameentry.delete(0,END)
            passwordentry.delete(0,END)
    else:
        print("There is no user present with the username",userentry)
        messagebox.showwarning("ERROR","No user present with that username")
        usernameentry.delete(0,END)
        passwordentry.delete(0,END)


def report():
    user_rep = usernameentry.get()
    bug_rep = bugentry.get()
    comm_rep = comments.get()

    add_report = ('''insert into reportdetails
    values (%s, %s, %s);''')
    data_report = (user_rep,bug_rep,comm_rep)
    cursor.execute(add_report,data_report)
    mc.commit()
    messagebox.showinfo("","issue reported successfully. Our team will look into it")
    bugentry.delete(0,END)
    comments.delete(0,END)
    f1.tkraise()       

def tocreateacc(): # raise create account frame

    f4.tkraise()

def backtotranslator(): # raise translator frame
    f1.tkraise()

def toaccountsettings(): # raise aoount settings frams
    f3.tkraise()

def tosupportedlanguages(): # open supported language text file
    os.startfile('supported_languages.txt')
    
def toreport(): # raise report screen
    f5.tkraise()

    # function to change properties of button on hover
def changeOnHover(button, colorOnHover, colorOnLeave):
  
    # adjusting backgroung of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover))
  
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave))


def tran():
    try:
        os.remove('sound.mp3')
    except:
        pass
    global translation_text_label
    global translation_text
    global x
    text = tranentry.get()
    lang = language.get()
    if text == '':
        messagebox.showwarning("ERROR","Please enter the text.")
        tranentry.delete(0,END)
    elif lang == '':
        messagebox.showwarning("ERROR","Please enter the text.")
        tranentry.delete(0,END)
    elif lang not in dval_list :
        messagebox.showwarning("ERROR","Please enter the correct language.")
        language.delete(0,END)
    else:
        
        x = invert.get(lang)
        translation_text = translator.translate(text, lang_tgt=x)
        translation_text_label=Label(flog,text=translation_text,font=('Arial',20),bg='white')
        translation_text_label.place(x=5,y=5)
        print(translation_text)
        audio3 = gTTS(text=translation_text , lang = x, slow=False)
        audio3.save("sound.mp3")
        playsound("sound.mp3")

        try : 
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            today = date.today()
            d = today.strftime("%d/%m/%Y")
            data = [d,current_time,text,lang,translation_text]


            historyfile = open("{}.csv".format(n),'a', encoding='utf-8')
            csvwriter = csv.writer(historyfile)
            csvwriter.writerow(data)
            historyfile.close()
        except:
            pass

def listen():
    playsound("sound.mp3")


def cleartext():
    try:
        text1_label.destroy()
        text_label.destroy()
        translation_text_label.destroy()
        os.remove('sound.mp3')
    except:
        pass

    
def history(): # opens user history csv file
    os.startfile("{}.csv".format(n))


def changeusername():
    newusername.delete(0,END)
    f31.tkraise()

def changepassword():
    newpassword.delete(0,END)
    oldpassword.delete(0,END)
    f32.tkraise()

def deleteaccount():
    f33.tkraise()

def deletehistory():
    f34.tkraise()

def delhisconfirm(): # delete history confirmed
    file = open("{}.csv".format(n),'w',encoding='utf-8')
    tempwriter = csv.writer(file)
    tempwriter.writerow(["Translation History data : "])
    tempwriter.writerow(['Date','Time','Original Text','Language','Translated Text'])
    file.close()
    f3.tkraise()
    messagebox.showinfo("","User translation history cleared successfully")

def helpg(): # raise help page
    f6.tkraise()

def cancel():
    f3.tkraise()

def history():
    openfile("{}.csv".format(n))

def confirm31():
    for t in range(1):
        changeusname = newusername.get()
        if changeusname in b:
            messagebox.showinfo("","Username already taken")
            RefreshUserList()
            f3.tkraise()
            break

        cursor.execute("update userdetails set username = '%s' where username = '%s'" %(changeusname,n))
        mc.commit()
        os.rename("{}.csv".format(n),"{}.csv".format(changeusname))
        print("username changed successfully")
        messagebox.showinfo("","Username changed successfully")
        RefreshUserList()
        logout()
        pass
    
def confirm32():
    opass = oldpassword.get()
    npass = newpassword.get()
    if w == opass:
        cursor.execute("update userdetails set password = '%s' where password = '%s'" %(npass,opass))
        mc.commit()
        print("Password successfully changed")
        messagebox.showinfo("","Password changed successfully")
        logout()
    else:
        print("Try entering password again")
        messagebox.showwarning("","Existing password does not match")
        newpassword.delete(0,END)
        oldpassword.delete(0,END)
    pass
    

def delac():
    cursor.execute("delete from userdetails where username = '%s'" %(n))
    mc.commit()
    os.remove("{}.csv".format(n))
    print('Account successfully deleted')
    messagebox.showinfo("","Account successfully deleted")
    RefreshUserList()
    logout()
    pass

def erase():
 
    translation_text_label.destroy()
    tranentry.delete(0,END)
    language.delete(0,END)



    
#FRAME2 IS THE LOGIN WINDOW FRAME ##########################################

f2 = Frame(root,width=750,height=500)
f2.place(x=0,y=0)
background = PhotoImage(file = 'bg1.png')
backlabel = Label(f2,image = background)
backlabel.grid(row=0,column=0)
logo = PhotoImage(file='logo3.png')
namelabel = Label(f2,image = logo)
namelabel.place(x=340,y=16)
# text widgets

textusername = Label(f2,text='USERNAME :',font=("Arial",12),bg='white',fg='black')
textusername.place(x=340,y=210)
textpassword = Label(f2,text='PASSWORD :',font=("Arial",12),bg='white',fg='black')
textpassword.place(x=340,y=280)
accounttext = Label(f2,text='Dont have an account ?',font=("Arial",15),bg='white',fg='black')
accounttext.place(x=340,y=420)
# button widgets 

createnewbutton = Button(f2,text='CREATE ONE',font=("Arial",10),bg = 'light green',command = tocreateacc)
createnewbutton.place(x=404,y=450)
loginbutton = Button(f2,text='LOGIN',font=("Arial",14),command=login,bg='light green',border = 2)

changeOnHover(loginbutton, "cyan" , 'light green')
loginbutton.place(x=500,y=370)
# entry widgets 
changeOnHover(createnewbutton, "cyan" , 'light green')


entryborder = Frame(f2,width = 277,height=44, bg= 'black')
entryborder.place(x=404,y=234)

entryborder = Frame(f2,width = 277,height=44, bg= 'black')
entryborder.place(x=404,y=304)

usernameentry = Entry(f2,font=('Arial',17))
usernameentry.place(x=410,y=240)
passwordentry = Entry(f2,font=('Arial',17),show='*')
passwordentry.place(x=410,y=310)


#FRAME1 is the translator page ##############################################

f1 = Frame(root,width=750,height=500)
f1.place(x=0,y=0)
backgroundf1 = PhotoImage(file = 'background1.png')
backlabelf1 = Label(f1,image = backgroundf1)
backlabelf1.grid(row=0,column=0)
logoutbutton = Button(f1,text='<<< LOGOUT',font=('Arial',10),border=5,command=logout,bg = 'light green')
logoutbutton.place(x=20,y=20)
changeOnHover(logoutbutton, "cyan" , 'light green')

welcomeborder = Frame(f1,width = 200,height=52, bg= 'cyan')
welcomeborder.place(x=275,y=15)
Welcometext = Label(f1,text='WELCOME!',font=('Arial',25),bg='black',fg='cyan')
Welcometext.place(x=280,y=20)

translateborder = Frame(f1,width = 312,height=50, bg= 'black')
translateborder.place(x=376,y=163)
translate = Label(f1,text='Enter the text to be translated :',font=("Arial",18),bg='black',fg='cyan')
translate.place(x=10,y=170)
tranentry = Entry(f1,font=('Arial',20))
tranentry.place(x=380,y=170)


langborder = Frame(f1,width = 312,height=50, bg= 'black')
langborder.place(x=300,y=230)
langtext = Label(f1,text='Select the language :',font=("Arial",18),bg='black',fg='cyan')
langtext.place(x=10,y=230)
language = Entry(f1,font=('Arial',20))
language.place(x = 304,y = 237)


translatebutton = Button(f1,text='Translate',font=('Arial',20),command = tran,bg='black',fg='cyan')
translatebutton.place(x=290,y=290)
changeOnHover(translatebutton, "grey" , 'black')

accountsettingsbutton = Button(f1,text='Account Settings',font=('Arial',15),bg = 'orange',border=5,command = toaccountsettings)
accountsettingsbutton.place(x=410,y=80)
changeOnHover(accountsettingsbutton, "light green" , 'orange')

tolanguages = Button(f1,text = 'Supported Languages',border=5,font = ('Arial',15),bg = 'orange',command=tosupportedlanguages)
tolanguages.place(x=170,y=80)

changeOnHover(tolanguages, "light green" , 'orange')


clear = Button(f1,text = 'clear',border=5,font = ('Arial',10),bg = 'black',fg = 'cyan',command=erase)
clear.place(x = 670,y=325)


listen = Button(f1,text = 'Listen',border=5,font = ('Arial',10),bg = 'black',fg = 'cyan',command=listen)
listen.place(x = 600,y=325)

changeOnHover(clear, "grey" , 'black')
changeOnHover(listen, "grey" , 'black')

######################## LOG FRAME #################################
logborder = Frame(f1,width = 663,height = 82,bg='black')
logborder.place(x=51,y=364)
flog = Frame(f1,width = 650,height=70,bg='White')
flog.place(x=58,y=370)

error = PhotoImage(file = 'report.png')
errorlabel = Button(f1,image=error,command=toreport)
errorlabel.place(x=650,y=70)

helpbut = Button(f1,text = 'Help',font=("Arial",15),bg = 'cyan',fg = 'black',command=helpg)
helpbut.place(x=670,y=20)
changeOnHover(helpbut, "grey" , 'cyan')

historybut = Button(f1,text = 'History',font=("Arial",15),bg = 'Black',fg = 'cyan',command = history)
historybut.place(x = 650,y=260)
changeOnHover(historybut, "grey" , 'black')

# FRAME 3 IS THE ACCOUNT SETTINGS PAGE ##########################


f3 = Frame(root,width=750,height=500)
f3.place(x=0,y=0)
backgroundf3 = PhotoImage(file = 'background2.png')
backlabelf3 = Label(f3,image = backgroundf3)
backlabelf3.grid(row=0,column=0)
back = Button(f3,text='<<< BACK TO TRANSLATOR',font=("Arial",10),border=5,command=backtotranslator,bg='light green',fg = 'black')
back.place(x=20,y=20)
changeOnHover(back, "cyan" , 'light green')
accsetborder = Frame(f3,width = 297,height=54, bg= 'cyan')
accsetborder.place(x=275,y=15)
accsettings = Label(f3,text = "ACCOUNT SETTINGS",font=('Arial',20),border=5,bg='black',fg='cyan')
accsettings.place(x=280,y=20)

changeusername = Button(f3,text="  Change your username  ",font=('Arial',20),command = changeusername,bg='black',fg='cyan')
changepassword = Button(f3,text="   Change your password   ",font=('Arial',20),command = changepassword,bg='black',fg='cyan')
delacc = Button(f3,text="    Delete your account     ",font=('Arial',20),command=deleteaccount,bg='black',fg = 'cyan')
delhistory = Button(f3,text="  Delete translation history  ",font=('Arial',20),command=deletehistory,bg='black',fg = 'cyan')
changeusername.place(x=20,y=170)
changepassword.place(x=370,y=170)
delacc.place(x=20,y=270)
delhistory.place(x=370,y=270)
changeOnHover(changeusername, "grey" , 'black')
changeOnHover(changepassword, "grey" , 'black')
changeOnHover(delacc, "grey" , 'black')
changeOnHover(delhistory, "grey" , 'black')

################   mini frames for different account settings:

################## change username


f31 = Frame(root,width = 450,height = 100,bg = 'white')
f31.place(x=170,y=360)

cancel31 = Button(f31,text = 'Cancel',font = ('Arial',14),command = cancel)
cancel31.place(x=120,y=50)

confirm31 = Button(f31,text = 'Confirm',font = ('Arial',14),command = confirm31)
confirm31.place(x=260,y=50)

changeOnHover(cancel31, "grey" , 'light grey')
changeOnHover(confirm31, "grey" , 'light grey')

newusername = Entry(f31,font = ("Arial",18),border=5)
newusername.place(x=160,y=5)
newusernamelabel= Label(f31,text = "New Username :",font = ("Arial",14),bg='white')
newusernamelabel.place(x=5,y=5)

################### change password

f32 = Frame(root,width = 550,height = 100,bg = 'white')
f32.place(x=120,y=360)

cancel32 = Button(f32,text = 'Cancel',font = ('Arial',14),command = cancel)
cancel32.place(x=450,y=10)

confirm32 = Button(f32,text = 'Confirm',font = ('Arial',14),command = confirm32)
confirm32.place(x=450,y=55)

oldpassword = Entry(f32,font = ("Arial",18),border=5)
oldpassword.place(x=160,y=5)
oldpasswordlabel= Label(f32,text = "Old password :",font = ("Arial",14),bg='white')
oldpasswordlabel.place(x=5,y=5)

newpassword = Entry(f32,font = ("Arial",18),border=5)
newpassword.place(x=160,y=50)
newpasswordlabel= Label(f32,text = "New password :",font = ("Arial",14),bg='white')
newpasswordlabel.place(x=5,y=50)

changeOnHover(cancel32, "grey" , 'light grey')
changeOnHover(confirm32, "grey" , 'light grey')

############################# delete account confirmation

f33 = Frame(root,width = 450,height = 100,bg = 'white')
f33.place(x=170,y=360)

confirmlabel = Label(f33,text='Are you sure you want to delete your account ?',font = ('Arial',14),bg='white')
confirmlabel.place(x=25,y=5)

confirm33 = Button(f33,text = 'Confirm',font = ('Arial',14),command = delac)
confirm33.place(x=260,y=50)

cancel33 = Button(f33,text = 'Cancel',font = ('Arial',14),command = cancel)
cancel33.place(x=120,y=50)

changeOnHover(cancel33, "grey" , 'light grey')
changeOnHover(confirm33, "grey" , 'light grey')

############################ confirmation for translation history 

f34 = Frame(root,width = 520,height = 100,bg = 'white')
f34.place(x=120,y=360)

confirmlabel34 = Label(f34,text='Are you sure you want to delete your translation history ?',font = ('Arial',14),bg='white')
confirmlabel34.place(x=25,y=5)

confirm34 = Button(f34,text = 'Confirm',font = ('Arial',14),command = delhisconfirm)
confirm34.place(x=300,y=50)

cancel34 = Button(f34,text = 'Cancel',font = ('Arial',14),command = cancel)
cancel34.place(x=150,y=50)

changeOnHover(cancel34, "grey" , 'light grey')
changeOnHover(confirm34, "grey" , 'light grey')

##########################   FRAME 4 IS THE CREATE NEW ACCOUNT PAGE###########
f4 = Frame(root,width=750,height = 500)
f4.place(x=0,y=0)
backgroundf4 = PhotoImage(file = 'background2.png')
backlabelf4 = Label(f4,image = backgroundf4)
backlabelf4.grid(row=0,column=0)

textmandt = Label(f4,text = "*Please fill each and every field",bg='black',fg='orange',font=('Arial',13) )
textmandt.place(x=60,y=350)

usernamecreate = Label(f4,text='ENTER USERNAME :',font=("Arial",18),bg='black',fg='cyan')
usernamecreate.place(x=60,y=150)
passwordcreate = Label(f4,text='ENTER PASSWORD :',font=("Arial",18),bg='black',fg='cyan')
passwordcreate.place(x=60,y=220)

passwordconfirm = Label(f4,text='CONFIRM PASSWORD :',font=("Arial",18),bg='black',fg='cyan')
passwordconfirm.place(x=60,y=290)

createacc = Label(f4,text = "CREATE YOUR LANGTRANS ACCOUNT",font=('Arial',20),border=5,bg='black',fg='cyan')
createacc.place(x=160,y=20)

userentry1border = Frame(f4,width = 311,height=50, bg= 'black')
userentry1border.place(x=376,y=143)
usernameentry1 = Entry(f4,font=('Arial',20))
usernameentry1.place(x=380,y=150)

passwordentry1border = Frame(f4,width = 313,height=50, bg= 'black')
passwordentry1border.place(x=376,y=213)
passwordentry1 = Entry(f4,font=('Arial',20),show='*')
passwordentry1.place(x=380,y=220)

confirmborder = Frame(f4,width = 313,height=50, bg= 'black')
confirmborder.place(x=376,y=283)
confirmpasswordentry = Entry(f4,font=('Arial',20),show='*')
confirmpasswordentry.place(x=380,y=290)


confirmbuttonborder = Frame(f4,width = 195,height=78, bg= 'black')
confirmbuttonborder.place(x=434,y=375)

confirm = Button(f4,text='CONFIRM',font=('Arial',25),command=submit,bg = 'light green',fg = 'black')
confirm.place(x=440,y=380)
changeOnHover(confirm,'cyan','light green')

gobacktologin = Button(f4,text='<<<<< BACK',font=("Arial",10),border=5,command=logout,bg='light green',fg = 'black')
gobacktologin.place(x=20,y=20)

changeOnHover(gobacktologin,'cyan','light green')


########################## frame 5 is the Report Errors page
f5 = Frame(root,width=750,height=500)
f5.place(x=0,y=0)
backgroundf5 = PhotoImage(file = 'background2.png')
backlabelf5 = Label(f5,image = backgroundf5)

backlabelf5.grid(row=0,column=0)

maintextborder = Frame(f5,width = 317,height=52, bg= 'cyan')
maintextborder.place(x=245,y=15)

maintext = Label(f5,text='REPORT AN ISSUE',font=('Arial',25),bg='black',fg='cyan')
maintext.place(x=250,y=20)

gobacktotrans = Button(f5,text='<<<<< BACK',font=("Arial",10),border=5,command=backtotranslator,bg='light green',fg = 'black')
gobacktotrans.place(x=20,y=20)

bugborder = Frame(f5,width = 313,height=50, bg= 'black')
bugborder.place(x=386,y=113)
bugentry = Entry(f5,font=('Arial',20))
bugentry.place(x=390,y=120)
writebug = Label(f5,text='REPORT AN ISSUE :',font=("Arial",20),bg='black',fg='cyan')
writebug.place(x=60,y=120)


commentsborder = Frame(f5,width = 313,height=50, bg= 'black')
commentsborder.place(x=386,y=283)
comments = Entry(f5,font=('Arial',20))
comments.place(x=390,y=290)
txt = Label(f5,text='COMMENTS/SUGGESTIONS :',font=("Arial",20),bg='black',fg='cyan')
txt.place(x=60,y=230)

submitborder = Frame(f5,width = 165,height=78, bg= 'black')
submitborder.place(x=304,y=375)
submit = Button(f5,text='SUBMIT',font=('Arial',25),command=report,bg = 'light green',fg = 'black')
submit.place(x=310,y=380)
changeOnHover(confirm,'cyan','light green')

############## frame 6 is the help page

f6 = Frame(root,width = 750,height=500)
f6.place(x=0,y=0)
backgroundf6 = PhotoImage(file = 'background1.png')
backlabelf6 = Label(f6,image = backgroundf6)
backlabelf6.grid(row=0,column=0)
helppage = PhotoImage(file='help.png')
namelabe2 = Label(f6,image = helppage)

text1 = Label(f6,text='Steps to use the language translator',font=('Arial',30),bg = 'black',fg = 'cyan')
text2 = Label(f6,text='1. Enter the text you want to translate into the text box.',font=('Arial',22),bg = 'black',fg = 'cyan')
text3 = Label(f6,text='2. Enter in a valid language in the second text box.',font=('Arial',22),bg = 'black',fg = 'cyan')
text4 = Label(f6,text='3. click on the "Translate" button to complete.',font=('Arial',22),bg = 'black',fg = 'cyan')

text1.place(x = 70,y=80)
text2.place(x=10,y=200)
text3.place(x=10,y=270)
text4.place(x=10,y=340)

goback = Button(f6,text='<<<<< BACK',font=("Arial",10),border=5,command=backtotranslator,bg='light green',fg='black')
goback.place(x=20,y=20)
changeOnHover(goback,'grey','light green')
# mainloop 
f2.tkraise()
root.mainloop()