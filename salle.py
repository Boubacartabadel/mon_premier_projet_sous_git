from tkinter import *
from tkinter import ttk, messagebox
#from PIL import Image, ImageTK
import time
import sqlite3
import os


class Salle:
    def __init__(self,root):
        background = "cyan"
        self.root = root
        self.root.title("Salle")
        self.root.geometry("650x300+70+70")
        self.root.config(bg=background)

        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS salle(Id INTEGER PRIMARY KEY AUTOINCREMENT ,Nom text)")
        con.commit()
        con.close()

        
        self.var_id = StringVar()
        self.var_salle = StringVar()


        self.salle = LabelFrame(self.root, text="Administration",font=("times new roman",15,"bold"),bg=background,bd=4, relief=GROOVE, width=1188, height=575)
        self.salle.place(x=5, y=0)
        
        lbl_salle = Label(self.salle, text="Salle", font=("times new roman",20,"bold"),bg=background).place(x=50, y=5)
        txt_salle = ttk.Entry(self.salle,textvariable=self.var_salle,font=("times new roman",18,"bold")).place(x=10, y=60, width=150)

        self.btn_ajouter = Button(self.salle, text="Ajouter",command=self.ajouter,font=("times new roman",15,"bold"),bg="green", cursor="hand2").place(x=180, y=60, width=100, height=30)
        self.btn_supprimer = Button(self.salle, text="Supprimer",command=self.supprimer,font=("times new roman",15,"bold"),bg="red", cursor="hand2").place(x=290, y=60, width=100, height=30)

        # Table 
        self.table = Frame(self.salle, bd=3, relief=RIDGE, bg=background)
        self.table.place(x=0, y=100, relwidth=1, height=170)

        #liste
        scroll_y = Scrollbar(self.table, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(self.table, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.salleliste = ttk.Treeview(self.table, columns=("Id","Nom"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
        
        scroll_x.config(command=self.salleliste.xview)
        scroll_y.config(command=self.salleliste.yview)

        self.salleliste.heading("Id", text="ID", anchor="w")
        self.salleliste.heading("Nom", text="Nom",anchor="w")
        
        self.salleliste["show"]="headings" 
        self.salleliste.pack(fill=BOTH, expand=1)

        self.salleliste.bind("<ButtonRelease-1>", self.obtenir_information)

        self.afficher()

    def ajouter(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            if self.var_id.get()=="":
                messagebox.showerror("erreur","Entrer le nom de la salle")
            else:
                cur.execute("insert into salle(Nom) values(?)",(
                self.var_salle.get(),
                ))
                con.commit()
                self.afficher()
                con.close()
                self.var_salle.set("")
                messagebox.showinfo("Succees","Enregistrement effectue avec succees")
        
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion a la base donnee {str(ex)}")
    def afficher(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            cur.execute("select * from salle")
            row = cur.fetchall()
            self.salleliste.delete(*self.salleliste.get_children())
            for rows in row :
                self.salleliste.insert("",END, values=rows)

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion a la base donnee {str(ex)}")

    def obtenir_information(self, ev):
        #self.btn_ajouter.config(state=NORMAL)
        #self.btn_supprimer.config(state=DISABLED)
        
        r = self.salleliste.focus()
        contenu = self.salleliste.item(r)
        row = contenu['values']

        self.var_id.set(row[0]),
        self.var_salle.set(row[1])

    def supprimer(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            op = messagebox.askyesno("avis","Voulez-vous vraiment supprimer")
            if op == True:
                cur.execute("delete from salle where Id=?",(self.var_id.get()
                ))
                con.commit()
                self.afficher()
                con.close()

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion a la base donnee {str(ex)}")


if __name__ =="__main__":
    root = Tk()
    obj = Salle(root)
    root.mainloop()
