from tkinter import *
from tkinter import ttk, messagebox
#from PIL import Image, ImageTK
import time
import sqlite3
import os
import random


class Client:
    def __init__(self,root):
        background = "cyan"
        self.root = root
        self.root.title("Client")
        self.root.geometry("1300x645+0+0")
        self.root.config(bg=background)

        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS client(Matricule INTEGER primary key,DSG text,Nom text,Prenom text,Pays text,Adresse text,Postal text,Type_Identite text,Numero_Identite text,Email text,Mobile text)")
        con.commit()
        con.close()

        self.frame_client = LabelFrame(self.root, text="Detail du client", font=("times new roman",15,"bold"),bg=background,bd=4, relief=GROOVE, width=1250, height=640)
        self.frame_client.place(x=5, y=0)

        # Zone de saisi
        self.frame_saisi = Frame(self.frame_client,bd=2, relief=RAISED,bg=background, width=500, height=500)
        self.frame_saisi.place(x=10, y=0)

        self.var_matricule = StringVar()
       # x = random(1000000, 9999999)  
       # self.var_matricule.set(str(x))

        self.var_dsg = StringVar()
        self.var_nom = StringVar()
        self.var_prenom = StringVar()
        self.var_adresse = StringVar()
        self.var_pays = StringVar()
        self.var_code_postal = StringVar()
        self.var_type_identite = StringVar()
        self.var_numero_identite = StringVar()
        self.var_email = StringVar()
        self.var_mobile = StringVar()
        
        



        # lbl_matricule
        lbl_matricule = Label(self.frame_saisi, text="Matricule", font=("times new roman",20,"bold"),bg=background).place(x=0,y=0)
        txt_matricule = Entry(self.frame_saisi, textvariable=self.var_matricule, font=("times new roman",20,"bold")).place(x=180,y=0, width=280)

        lbl_dsg = Label(self.frame_saisi, text="DS/G", font=("times new roman",20,"bold"),bg=background).place(x=0,y=40)
        txt_dsg = Entry(self.frame_saisi,textvariable=self.var_dsg, font=("times new roman",20,"bold")).place(x=180,y=40, width=280)

        lbl_nom = Label(self.frame_saisi, text="Nom", font=("times new roman",20,"bold"),bg=background).place(x=0,y=80)
        txt_nom = Entry(self.frame_saisi,textvariable=self.var_nom, font=("times new roman",20,"bold")).place(x=180,y=80, width=280)

        lbl_prenom = Label(self.frame_saisi, text="Prenom", font=("times new roman",20,"bold"),bg=background).place(x=0,y=120)
        txt_prenom = Entry(self.frame_saisi,textvariable=self.var_prenom, font=("times new roman",20,"bold")).place(x=180,y=120, width=280)

        lbl_pays = Label(self.frame_saisi, text="Adresse", font=("times new roman",20,"bold"),bg=background).place(x=0,y=160)
        txt_pays = Entry(self.frame_saisi,textvariable=self.var_pays, font=("times new roman",20,"bold")).place(x=180,y=160, width=280)

        lbl_adresse = Label(self.frame_saisi, text="Pays", font=("times new roman",20,"bold"),bg=background).place(x=0,y=200)
        txt_adresse = Entry(self.frame_saisi,textvariable=self.var_adresse, font=("times new roman",20,"bold")).place(x=180,y=200, width=280)

        lbl_code = Label(self.frame_saisi, text="Code postal", font=("times new roman",20,"bold"),bg=background).place(x=0,y=240)
        txt_code = Entry(self.frame_saisi,textvariable=self.var_code_postal, font=("times new roman",20,"bold")).place(x=180,y=240, width=280)

        lbl_type_identite = Label(self.frame_saisi, text="Type_identite ", font=("times new roman",20,"bold"),bg=background).place(x=0,y=280)
        txt_type_identite = ttk.Combobox(self.frame_saisi,values=["CNI","PASSPORT"], state="r",textvariable=self.var_type_identite, justify=CENTER,font=("times new roman",20,"bold"))
        txt_type_identite.current(0)
        txt_type_identite.place(x=180, y=280, width=280, height=40)

        lbl_numero_identite = Label(self.frame_saisi, text="No Identite", font=("times new roman",20,"bold"),bg=background).place(x=0,y=325)
        txt_numero_identite = Entry(self.frame_saisi,textvariable=self.var_numero_identite, font=("times new roman",20,"bold")).place(x=180,y=325, width=280)

        lbl_email = Label(self.frame_saisi, text="Email", font=("times new roman",20,"bold"),bg=background).place(x=0,y=365)
        txt_email = Entry(self.frame_saisi,textvariable=self.var_email, font=("times new roman",20,"bold")).place(x=180,y=365, width=280)

        
        lbl_mobile = Label(self.frame_saisi, text="Mobile", font=("times new roman",20,"bold"),bg=background).place(x=0,y=405)
        txt_mobile = Entry(self.frame_saisi,textvariable=self.var_mobile, font=("times new roman",20,"bold")).place(x=180,y=405, width=280)

        
        

        # bouton
        self.frame_bouton = Frame(self.frame_client, bd=2, bg=background, relief=RAISED, width=500, height=50)
        self.frame_bouton.place(x=10, y=540)

        self.btn_ajouter = Button(self.frame_bouton, text="Ajouter",command=self.ajouter,font=("times new roman",15,"bold"),bg="green", cursor="hand2")
        self.btn_ajouter.place(x=20, y=5,width=100)

        self.btn_modifier = Button(self.frame_bouton,command=self.modifier, text="Modifier",font=("times new roman",15,"bold"),state=DISABLED,bg="yellow", cursor="hand2")
        self.btn_modifier.place(x=140,y=5,width=100)

        self.btn_supprimer = Button(self.frame_bouton,command=self.supprimer, text="Supprimer",font=("times new roman",15,"bold"),state=DISABLED,bg="red", cursor="hand2")
        self.btn_supprimer.place(x=260, y=5,width=100)

        self.btn_reinitiliser = Button(self.frame_bouton, text="Reinitiliser",command=self.reinitiliser
        ,font=("times new roman",15,"bold"),bg="gray", cursor="hand2")
        self.btn_reinitiliser.place(x=380, y=5,width=100)

        # Zone d'affichage
        self.frame_table = Frame(self.frame_client, bd=2, relief=RAISED,bg=background, width=700, height=500)
        self.frame_table.place(x=515, y=0)

        self.frame_recherche = LabelFrame(self.frame_table, text="Recherche par",font=("times new roman",15,"bold"),bg=background, width=680, height=100)
        self.frame_recherche.place(x=10,y=10)

       # declaration de variable 
        self.var_type_recherche = StringVar()
        self.var_recherche_par = StringVar()

        txt_type_identite = ttk.Combobox(self.frame_table,values=["Nom","Prenom","Mobile"], state="r",textvariable=self.var_type_recherche, justify=CENTER,font=("times new roman",20,"bold"))
        txt_type_identite.current(0)
        txt_type_identite.place(x=10, y=50, width=180, height=40)

        txt_recherche_par = ttk.Entry(self.frame_table,textvariable=self.var_recherche_par, font=("times new roman",20,"bold")).place(x=200, y=55, width=180)

        btn_recherche = Button(self.frame_table,command=self.recherche, text="Recherche",font=("times new roman",20,"bold"),bg="lightgray",cursor="hand2").place(x=390,y=55 , height=30)

        btn_tous = Button(self.frame_table, text="Tous",command=self.afficher,font=("times new roman",20,"bold"),bg="lightgray",cursor="hand2").place(x=550,y=55 , height=30)

        #liste
        self.frame_tree = Frame(self.frame_table, bd=2, relief=RIDGE, bg=background)
        self.frame_tree.place(x=0,y=120, width=690, height=370)

        scroll_y = Scrollbar(self.frame_tree, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(self.frame_tree, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.clientliste = ttk.Treeview(self.frame_tree, columns=("Matricule","DSG","Nom","Prenom","Adresse","Pays","Postal","Type_Identite","Numero_Identite","Email","Mobile"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
        
        scroll_x.config(command=self.clientliste.xview)
        scroll_y.config(command=self.clientliste.yview)

        self.clientliste.heading("Matricule", text="Matricule")
        self.clientliste.heading("DSG", text="DSG")
        self.clientliste.heading("Nom", text="Nom")
        self.clientliste.heading("Prenom", text="Prenom")
        self.clientliste.heading("Adresse", text="Adresse")
        self.clientliste.heading("Pays", text="Pays")
        self.clientliste.heading("Postal", text="Postal")
        self.clientliste.heading("Type_Identite", text="Type_Identite")
        self.clientliste.heading("Numero_Identite", text="Numero_Identite")
        self.clientliste.heading("Email", text="Email")
        self.clientliste.heading("Mobile", text="Mobile")
        
        self.clientliste["show"]="headings" 
        self.clientliste.pack(fill=BOTH, expand=1)
        self.clientliste.bind("<ButtonRelease-1>", self.obtenir_information)

        self.afficher() 

    def ajouter(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            if self.var_nom.get()=="" or self.var_prenom.get()=="" or self.var_mobile.get()=="" or self.var_type_identite.get()=="":
                messagebox.showerror("Erreur","Veillez remplir les champs obligatoire. ")
            else:
                cur.execute("select * from client where Matricule=?",(self.var_matricule.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Erreur", "Le matricule existe deja")
                else:
                    cur.execute("insert into client(Matricule,DSG,Nom,Prenom,Adresse,Pays,Postal,Type_Identite,Numero_Identite,Email,Mobile) values(?,?,?,?,?,?,?,?,?,?,?)",(
                        self.var_matricule.get(),
                        self.var_dsg.get(),
                        self.var_nom.get(), 
                        self.var_prenom.get(),
                        self.var_adresse.get(),
                        self.var_pays.get(), 
                        self.var_code_postal.get(),
                        self.var_type_identite.get(), 
                        self.var_numero_identite.get(), 
                        self.var_email.get(),
                        self.var_mobile.get()
                        
                    ))
                    con.commit()
                    con.close()
                    self.afficher()
                    self.reinitiliser()
                    messagebox.showinfo("Success","Ajout effectuer avec success!")
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion  {str(ex)}")


    def afficher(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            cur.execute("select * from client")
            rows = cur.fetchall()
            self.clientliste.delete(*self.clientliste.get_children())
            for row in rows:
                self.clientliste.insert("",END, values=row)
           
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion  {str(ex)}")
    
    def obtenir_information(self, ev):
        self.btn_ajouter.config(state=DISABLED)
        self.btn_modifier.config(state=NORMAL)
        self.btn_supprimer.config(state=NORMAL)
        r = self.clientliste.focus()
        contenu = self.clientliste.item(r)
        row = contenu['values']
        self.var_matricule.set(row[0]),
        self.var_dsg.set(row[1]),
        self.var_nom.set(row[2]),     
        self.var_prenom.set(row[3]),
        self.var_adresse.set(row[4]),
        self.var_pays.set(row[5]), 
        self.var_code_postal.set(row[6]),
        self.var_type_identite.set(row[7]), 
        self.var_numero_identite.set(row[8]), 
        self.var_email.set(row[9]),
        self.var_mobile.set(row[10])

    def reinitiliser(self):
        self.btn_ajouter.config(state=NORMAL)
        self.btn_modifier.config(state=DISABLED)
        self.btn_supprimer.config(state=DISABLED)
        self.var_matricule.set(""),
        self.var_dsg.set(""),
        self.var_nom.set(""),
        self.var_prenom.set(""),
        self.var_adresse.set(""),
        self.var_pays.set(""), 
        self.var_code_postal.set(""),
        self.var_type_identite.set("CNI"), 
        self.var_numero_identite.set(""), 
        self.var_email.set(""),
        self.var_mobile.set("")

    def modifier(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            cur.execute("update client set DSG=?,Nom=?,Prenom=?,Pays=?,Adresse=?,Postal=?,Type_Identite=?,Numero_Identite=?,Email=?,Mobile=? where Matricule=? ",(
                self.var_dsg.get(),
                self.var_nom.get(),
                self.var_prenom.get(),
                self.var_adresse.get(),
                self.var_pays.get(), 
                self.var_code_postal.get(),
                self.var_type_identite.get(), 
                self.var_numero_identite.get(), 
                self.var_email.get(),
                self.var_mobile.get(),
                self.var_matricule.get()

            ))
            con.commit()
            con.close()
            self.afficher()
            self.reinitiliser()
            messagebox.showinfo("Success","Modification effectuer avec success!")

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion  {str(ex)}")
    

    def supprimer(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            op = messagebox.askyesno("Confirmer","Voulez-vous vraiment supprimer ce client")
            if op ==True:
                cur.execute("delete from client where Matricule=?",(self.var_matricule.get(),))
                con.commit()
                con.close()
                self.afficher()
                self.reinitiliser()
                messagebox.showinfo("Supprimer", "Suppression effectue avec success!")

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion  {str(ex)}")
    
   
    def recherche(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            if self.var_recherche_par.get()=="":
                messagebox.showinfo("Erreur","Veillez saisir  les champs")
            else:
                cur.execute("select * from client where "+self.var_type_identite.get()+" LIKE '%"+self.var_recherche_par.get()+"%'")
                row = cur.fetchall()
                if len(row)!=0:
                    self.clientliste.delete(*self.clientliste.get_children())
                    for rows in row:
                        self.clientliste.insert("",END, values=rows)
                else:
                    messagebox.showerror("Erreur","Aucun trouvé")  
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")


       




if __name__ =="__main__":
    root = Tk()
    obj = Client(root)
    root.mainloop()
