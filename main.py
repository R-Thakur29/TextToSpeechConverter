import mysql.connector
from mysql.connector import Error
from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image,ImageTk
#from tkinter import combobox
import pyttsx3
import os
import threading
import PyPDF2
import addlan

root=tk.Tk()
root.title("Text to Speech Convertor")
root.geometry("900x550+200+100")
root.resizable(False,False)
root.configure(bg="#305063")

engine = pyttsx3.init()

def combobox():
    connection = mysql.connector.connect(host='localhost', database='TTS', user='root', password='*****')
    if connection.is_connected():
        cursor = connection.cursor()

        dp="select L_Name from language"
        cursor.execute(dp)
        data3=cursor.fetchall()   

        cursor.close()
        connection.close()

    #To Change Language 
    global lan
    lan=ttk.Combobox(root,values=data3,font="arial 14",state='readonly',width=10)
    lan.place(x=640, y=50)
    lan.set(data3[0])



def db():
    try:
        connection = mysql.connector.connect(host='localhost',
                                                database='TTS',
                                                user='root',
                                                password='*****')
        if connection.is_connected():
            cursor = connection.cursor()

            Lan=lan.get()
            m_id="Select Male_id from Language where L_Name='"+Lan+"'"
            f_id="Select Female_id from Language where L_Name='"+Lan+"'"

            cursor.execute(m_id)
            data1=cursor.fetchone()
            cursor.execute(f_id)
            data2=cursor.fetchone()
            connection.commit()
            global i,j
                 
            
            i=data1[0]
            j=data2[0]


    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    


def open_pdf():
    pdffile = filedialog.askopenfilename()
    pdffile = open(pdffile,'rb')

    readpdf = PyPDF2.PdfReader(pdffile)

    for i in range(0,len(readpdf.pages)):
        page = readpdf.pages[i]
        TExt = page.extract_text()
        Text_area.insert(END,TExt)
        
    pdffile.close()


def open_file():
    Text_file = filedialog.askopenfilename(title="open file")
    Text_file = open(Text_file,'r')
    Text = Text_file.read()

    Text_area.insert(END,Text)
    Text_file.close()


def speaknow():
    db()
    Text = Text_area.get(1.0, END)
    Gender = gender.get()
    Speed = speed.get()
    voices = engine.getProperty('voices')
    engine.setProperty('volume',(scale_level.get()) / 100)
   

    def setvoice():
        if(Gender == 'Male'):
           engine.setProperty('voice',voices[i].id)
           engine.say(Text)
           engine.runAndWait()
           engine.stop()
        else:
           engine.setProperty('voice',voices[j].id)
           engine.say(Text)
           engine.runAndWait()
           engine.stop()

    if len(Text)>1:
        if(Speed == "Fast"):
            engine.setProperty('rate',250)
            setvoice()
        elif(Speed == "Normal"):
            engine.setProperty('rate',170)
            setvoice()
        else:
            engine.setProperty('rate',60)
            setvoice()

    else:
        messagebox.showwarning("Warning","First Enter Some Text")        

def download():
    Text = Text_area.get(1.0, END)
    Gender = gender.get()
    Speed = speed.get()
    voices = engine.getProperty('voices')
    
    def setvoice():
        if(Gender == 'Male'):
           engine.setProperty('voice',voices[i].id)         
        else:
           engine.setProperty('voice',voices[j].id)
           
    if len(Text)>1:       
        if(Speed == "Fast"):
            engine.setProperty('rate',250)
            setvoice()
        elif(Speed == "Normal"):
            engine.setProperty('rate',170)
            setvoice()
        else:
            engine.setProperty('rate',60)
            setvoice()
    else:
        messagebox.showwarning("Warning","First Enter Some Text") 

    Filename = filedialog.asksaveasfilename( defaultextension=".mp3")
    engine.save_to_file(Text,Filename)
    messagebox.showinfo('Successfull','Audio is Saved')
    engine.runAndWait()
    engine.stop()

#icon
image_icon=PhotoImage(file='logo.png')
root.iconphoto(False ,image_icon)

#Labels
Label(root,text="VOICE",font="arial 15 bold",bg="#305063",fg="white").place(x=580,y=100)
Label(root,text="SPEED",font="arial 15 bold",bg="#305063",fg="white").place(x=760,y=100)
Label(root,text="VOLUME",font="arial 15 bold",bg="#305063",fg="white").place(x=665,y=190)
Label(root,text="LANGUAGE",font="arial 15 bold",bg="#305063",fg="white").place(x=650,y=20)

scrol_bar=Scrollbar(root,orient=VERTICAL)
scrol_bar.place(x=510,y=50,width=16,height=390)
Text_area=Text(root,font="Rpbote 20",bg="white",yscrollcommand=scrol_bar.set,relief=GROOVE,wrap=WORD)
Text_area.place(x=10,y=50,width=500,height=390)
scrol_bar.config(command=Text_area.yview)

#To change the Gender of the Voice 
gender=ttk.Combobox(root,values=['Male','Female'],font="arial 14",state='readonly',width=10)
gender.place(x=550, y=130)
gender.set('Male')

#To Change the Rate of Voice 
speed=ttk.Combobox(root,values=['Slow','Normal','Fast'],font="arial 14",state='readonly',width=10)
speed.place(x=730, y=130)
speed.set('Normal')

#Speak button
s_btn=Button(root,text="Speak",width=10,font="arial 16 bold",bg='lime',activebackground='yellow',relief=SUNKEN,bd=5,command=lambda: threading.Thread(target=speaknow, daemon=True).start())
s_btn.place(x=550 ,y=290)

#Download button
d_btn=Button(root,text='Download',width=10,font='arial 16 bold ',relief=SUNKEN,bg='lime',activebackground='yellow',bd=5,command=download)
d_btn.place(x=645,y=370)

#clear Button to clear text
c_btn=Button(root,text='Clear',width=10,font='arial 16 bold ',relief=SUNKEN,bg='lime',activebackground='yellow',bd=5,command=lambda: Text_area.delete(0.0,END))
c_btn.place(x=730,y=290)

#Volume 
scale_level=Scale(root,from_=0,to=100,bg='#305063',orient=HORIZONTAL,length=160)
scale_level.place(x=630 ,y=220)
scale_level.set(50)

#import file
s_btn=Button(root,text="Import text file",width=10,font="arial 16 bold",bg='lime',activebackground='yellow',relief=SUNKEN,bd=5,command=open_file)
s_btn.place(x=20 ,y=470)

#import pdf
s_btn=Button(root,text="Import pdf",width=10,font="arial 16 bold",bg='lime',activebackground='yellow',relief=SUNKEN,bd=5,command=open_pdf)
s_btn.place(x=230 ,y=470)

#Add Language
s_btn=Button(root,text="Add language",width=10,font="arial 16 bold",bg='lime',activebackground='yellow',relief=SUNKEN,bd=5,command=addlan.AddLan)
s_btn.place(x=440 ,y=470)

combobox()
root.mainloop()