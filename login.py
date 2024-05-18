from tkinter import *
from tkinter import ttk, messagebox
#from PIL import Image, ImageTK
import time
import sqlite3
import os


class Login:
    def __init__(self,root):
        background = "cyan"
        self.root = root
        self.root.title("Login")
        self.root.geometry("1000x500+70+70")
        self.root.config(bg=background)

        
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
       

        self.var_nom_user = StringVar()
        self.var_password = StringVar()

        titre = Label(self.root, text="Page de Connexion", font=("times new roman",20,"bold"),bg=background).pack()
        self.frame_login = Frame(self.root, bd=3, relief=GROOVE, bg="lightgreen")
        self.frame_login.place(x=250, y=50, width=500, height=400)

        lbl_user = Label(self.root, text="User", font=("times new roman",20), bg="lightgreen").place(x=460,y=140)
        txt_user = ttk.Entry(self.root,textvariable=self.var_nom_user, font=("times new roman",18)).place(x=430,y=180, width=200)

        lbl_password = Label(self.root, text="Password", font=("times new roman",20), bg="lightgreen").place(x=460,y=220)
        txt_password = ttk.Entry(self.root,show=["*"], textvariable=self.var_password, font=("times new roman",18)).place(x=430,y=260, width=200)

        self.btn_connexion = Button(self.root, command=self.connexion, text="Connexion", font=("times new roman",20), bg="lightblue", cursor="hand2").place(x=460,y=340, height=40)

    def connexion(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        
        try:
            if self.var_nom_user.get()=="" or self.var_password.get()=="":
                messagebox.showerror("Erreur","Entrez le nom_user et password")
            else:
                cur.execute("select Role from Admin where Login=? and Password=?",(self.var_nom_user.get(),self.var_password.get()))
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror("Erreur","user / password n'existent pas ")
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        import administrateur
                        #os.system("python C:/Users/hp 8470p/Desktop/Reservation_en_Python/Reservation/administrateur.py")
                    else:
                        self.root.destroy()
                        import home
                        #os.system("python C:/Users/hp 8470p/Desktop/Reservation_en_Python/Reservation/home.py")
                    

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion a la base de donnee {stsr(ex)}")    
        

if __name__ =="__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()
