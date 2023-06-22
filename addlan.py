from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error


def AddLan():
    root=tk.Tk()
    root.title("Text to Speech Convertor")
    root.geometry("900x550+200+100")
    root.resizable(False,False)
    root.configure(bg="#305063")

    def show():
        connection = mysql.connector.connect(host='localhost',
                                                database='TTS',
                                                user='root',
                                                password='*****')
        cursor = connection.cursor()
        cursor.execute("SELECT L_Name,Male_id,Female_id FROM language")
        records = cursor.fetchall()

        for i, (Language,Male_id,Female_id) in enumerate(records, start=1):
            listBox.insert("", "end", values=(Language,Male_id,Female_id))
            cursor.close()

    def Add():
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='TTS',
                                                user='root',
                                                password='*****')
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()

                lan_name=e1.get()
                m_id=e2.get()
                f_id=e3.get()

                insert_query = "INSERT INTO `language` (`L_Name`, `Male_id`, `Female_id`) VALUES( %s,%s,%s)"               
                vals = (lan_name,m_id,f_id)
                cursor.execute(insert_query,vals)
                connection.commit()

                messagebox.showinfo("information", "Language Added successfully...")

                e1.delete(0, END)
                e2.delete(0, END)
                e3.delete(0, END)
                e1.focus_set()


        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

        listBox.delete(*listBox.get_children())
        show()

    def delete():
        lang = e1.get()

        connection=mysql.connector.connect(host="localhost",user="root",password="*****",database="TTS")
        cursor=connection.cursor()

        try:
            sql = "delete from language where L_Name = %s"
            val = (lang,)
            cursor.execute(sql, val)
            connection.commit()
            lastID = cursor.lastrowid
            messagebox.showinfo("information", "Language Deleted successfully...")

            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e1.focus_set()

        except Exception as e:

            print(e)
            connection.rollback()
            connection.close()
            cursor.close()
            listBox.delete(*listBox.get_children())
            show()

    def update():
        lang = e1.get()
        m_id = e2.get()
        f_id = e3.get()
        connection=mysql.connector.connect(host="localhost",user="root",password="*****",database="TTS")
        cursor=connection.cursor()

        try:
            sql = "Update  language set Male_id= %s,Female_id= %s where L_Name= %s"
            val = (m_id,f_id,lang)
            cursor.execute(sql, val)
            connection.commit()
            lastID = cursor.lastrowid
            messagebox.showinfo("information", "Language Updated successfully...")

            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e1.focus_set()

        except Exception as e:

            print(e)
            connection.rollback()
            connection.close()
            cursor.close()
            listBox.delete(*listBox.get_children())
            show()

    def getrow(event):
        row_id = listBox.identify_row(event.y)
        item = listBox.item(listBox.focus())
        t1.set(item['values'][0])
        t2.set(item['values'][1])
        t3.set(item['values'][2])
        print(row_id)

    t1 = StringVar()
    t2 = StringVar()
    t3 = StringVar()

    Label(root,text="Language :",font="arial 15 bold",bg="#305063",fg="white").place(x=30,y=150)
    Label(root,text="Male ID :",font="arial 15 bold",bg="#305063",fg="white").place(x=50,y=210)
    Label(root,text="Female ID :",font="arial 15 bold",bg="#305063",fg="white").place(x=30,y=270)

    c_btn=Button(root,text='ADD',width=10,font='arial 16 bold ',relief=SUNKEN,bg='lime',activebackground='yellow',bd=5,command=Add)
    c_btn.place(x=200,y=380)

    c_btn=Button(root,text='Delete',width=10,font='arial 16 bold ',relief=SUNKEN,bg='lime',activebackground='yellow',bd=5,command=delete)
    c_btn.place(x=30,y=380)

    c_btn=Button(root,text='Update',width=10,font='arial 16 bold ',relief=SUNKEN,bg='lime',activebackground='yellow',bd=5,command=update)
    c_btn.place(x=370,y=380)



    e1 = tk.Entry(root,font=('Arial 14'),width=15,textvariable=t1)
    e2 = tk.Entry(root,font=('Arial 14'),width=15,textvariable=t2)
    e3 = tk.Entry(root,font=('Arial 14'),width=15,textvariable=t3)

    e1.place(x=160,y=152)
    e2.place(x=160,y=212)
    e3.place(x=160,y=272)

    style=ttk.Style()
    style.theme_use('default')
    cols = ('Language', 'Male_Id', 'Female_Id') 
    listBox = ttk.Treeview(root, columns=cols, show='headings')
    listBox.place(x=400, y=130)
    for col in cols:
        listBox.heading(col, text=col)
        listBox.column(col, stretch=NO, anchor=CENTER, width=150)
    
    listBox.bind('<Double 1>',getrow)

    show()
    root.mainloop()

