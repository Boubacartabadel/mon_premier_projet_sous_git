from tkinter import *
from tkinter import ttk, messagebox
#from PIL import Image, ImageTK
import time
import sqlite3
import os
import tempfile
from tkcalendar import *
from datetime import datetime
from time import strftime


class Reservation:
    def __init__(self,root):
        background = "cyan"
        self.root = root
        self.root.title("Reservation")
        self.root.geometry("1200x558+90+90")
        self.root.config(bg=background)


        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS reservation(Id INTEGER PRIMARY KEY AUTOINCREMENT, Mobile text,Date_debut date,Date_fin date,Type_salle text,Nom_salle text,Nombre_place text,Type_activite text,Prix_salle text,Nombre_jour text,Total_payer text)")
        con.commit()
        con.close()

        self.liste_facture = []
        self.liste_salle = []
        self.listesalle()

        self.var_id = StringVar()
        self.var_mobile = StringVar()
        self.var_type_salle = StringVar()
        self.var_nom_salle = StringVar()
        self.var_nombre_place = StringVar()
        self.var_type_activite = StringVar()
        self.var_prix_salle = StringVar()
        self.var_nombre_jour = StringVar()
        self.var_total_a_payer = StringVar()




        self.frame_reservation = LabelFrame(self.root, text="Reservation", bg=background, bd=3, relief=RIDGE, font=("times new roman",20,"bold"), width=1188, height=550)
        self.frame_reservation.place(x=0, y=0)

        # Zone de saisi 
        self.frame_saisi = Frame(self.frame_reservation, bd=2, relief=GROOVE,bg=background, width=387, height=410)
        self.frame_saisi.place(x=0, y=0)

        lbl_matricule = Label(self.frame_saisi, text="Mobile", font=("times new roman",20,"bold"),bg=background).place(x=0,y=5)
        txt_matricule = ttk.Entry(self.frame_saisi,textvariable=self.var_mobile, font=("times new roman",17,"bold")).place(x=90,y=7, width=130, height=27)

        btn_identifier = Button(self.frame_saisi,command=self.verifie_identite, text="verifIdentite",font=("times new roman",15,"bold"), cursor="hand2").place(x=230, y=7,height=27)

        lbl_date_debut =  Label(self.frame_saisi, text="Date debut", font=("times new roman",20,"bold"),bg=background).place(x=0,y=45)
        self.var_date_debut = DateEntry(self.frame_saisi, font=("times new roman",20),date_pattern="dd/mm/yy", justify=CENTER, state="r")
        self.var_date_debut.place(x=180, y=45, width=150)

        lbl_date_fin =  Label(self.frame_saisi, text="Date fin", font=("times new roman",20,"bold"),bg=background).place(x=0,y=95)
        self.var_date_fin = DateEntry(self.frame_saisi, font=("times new roman",20),date_pattern="dd/mm/yy", justify=CENTER, state="r")
        self.var_date_fin.place(x=180, y=90, width=150)

        lbl_nombre_place = Label(self.frame_saisi, text="Type  salle", font=("times new roman",20,"bold"),bg=background ).place(x=0,y=130)
        txt_nombre_place = ttk.Entry(self.frame_saisi,textvariable=self.var_type_salle, font=("times new roman",17)).place(x=180,y=130, width=170, height=27)

        

        lbl_nom_salle =  Label(self.frame_saisi, text="Nom salle", font=("times new roman",20,"bold"),bg=background).place(x=0,y=165)
        txt_nom_salle = ttk.Combobox(self.frame_saisi,textvariable=self.var_nom_salle,font=("times new roman",17), values=self.liste_salle, justify=CENTER, state="r")
        txt_nom_salle.current(0)
        txt_nom_salle.place(x=180, y=170, width=170)

        lbl_nombre_place = Label(self.frame_saisi, text="Nombre  place", font=("times new roman",20,"bold"),bg=background ).place(x=0,y=200)
        txt_nombre_place = ttk.Entry(self.frame_saisi,textvariable=self.var_nombre_place, font=("times new roman",17)).place(x=180,y=210, width=170, height=27)

        lbl_type_active = Label(self.frame_saisi, text="Type active", font=("times new roman",20,"bold"),bg=background ).place(x=0,y=235)
        txt_type_active = ttk.Entry(self.frame_saisi,textvariable=self.var_type_activite, font=("times new roman",17)).place(x=180,y=240, width=170, height=27)

        lbl_prix_salle = Label(self.frame_saisi, text="Prix salle", font=("times new roman",20,"bold"),bg=background ).place(x=0,y=270)
        txt_prix_salle = ttk.Entry(self.frame_saisi,textvariable=self.var_prix_salle, font=("times new roman",17)).place(x=180,y=275, width=170, height=27)

        lbl_nombre_jour = Label(self.frame_saisi, text="Nombre jour(s)", font=("times new roman",20,"bold"),bg=background).place(x=0,y=305)
        self.txt_nombre_jour = Label(self.frame_saisi,text="", font=("times new roman",17),bg="lightgray")
        self.txt_nombre_jour.place(x=180,y=315, width=170, height=27)

        lbl_total = Label(self.frame_saisi, text="Total a payer", font=("times new roman",20,"bold"),bg=background).place(x=0,y=345)
        txt_total = ttk.Entry(self.frame_saisi,textvariable=self.var_total_a_payer, state="r",font=("times new roman",20,"bold")).place(x=180,y=350, width=170, height=27)

        self.btn_ajouter = Button(self.frame_saisi,command=self.facture, text="Facture",font=("times new roman",15,"bold"),bg="lightyellow", cursor="hand2")
        self.btn_ajouter.place(x=40, y=377, height=35)





        # Zone boutton 
        self.frame_bouton = Frame(self.frame_reservation, bd=2, bg=background, relief=RAISED, width=387, height=100)
        self.frame_bouton.place(x=0, y=410)
        # btn
        self.btn_ajouter = Button(self.frame_bouton, state=NORMAL, text="Reserver",command=self.reservation,font=("times new roman",15,"bold"),bg="green", cursor="hand2")
        self.btn_ajouter.place(x=10, y=0,width=150)

        self.btn_modifier = Button(self.frame_bouton,state=DISABLED,  text="Modifier",command=self.modifier,font=("times new roman",15,"bold"),bg="yellow", cursor="hand2")
        self.btn_modifier.place(x=190, y=0,width=150)

        self.btn_annuler = Button(self.frame_bouton, state=DISABLED,  text="Annuler",command=self.supprimer,font=("times new roman",15,"bold"),bg="red", cursor="hand2")
        self.btn_annuler.place(x=10, y=50,width=150)

        self.btn_reinitiliser = Button(self.frame_bouton,command=self.reinitiliser, text="Reinitialiser",font=("times new roman",15,"bold"),bg="lightgray", cursor="hand2")
        self.btn_reinitiliser.place(x=190, y=50,width=150)


        # Zone affichage 
        self.frame_affichage = Frame(self.frame_reservation, bd=2, bg=background, relief=RAISED, width=870, height=510)
        self.frame_affichage.place(x=390, y=0)
        
        # Zone affichage identite
        self.frame_affiche_identite = Frame(self.frame_affichage, bd=2, bg=background, relief=RAISED, width=792, height=100)
        self.frame_affiche_identite.place(x=0, y=0)
       
        # Zone affichage recherche
        self.var_type_recherche = StringVar()
        self.var_recherche = StringVar()

        self.frame_recherche = LabelFrame(self.frame_affichage, text="Recherche", bg=background, bd=3, relief=RIDGE, font=("times new roman",20,"bold"), width=795, height=100)
        self.frame_recherche.place(x=0, y=99)

        type_recherche = ttk.Combobox(self.frame_recherche,textvariable=self.var_type_recherche,font=("times new roman",20,"bold"), values=["Facture","Mobile","Date_debut","Nom_salle"], justify=CENTER, state="r")
        type_recherche.current(0)
        type_recherche.place(x=0, y=2, width=150)

        recherche = ttk.Entry(self.frame_recherche,textvariable=self.var_recherche,font=("times new roman",20,"bold")).place(x=160, y=2, width=150)

        self.btn_recherche = Button(self.frame_recherche,command=self.recherche, text="Recherche",font=("times new roman",15,"bold"),bg="lightgreen", cursor="hand2")
        self.btn_recherche.place(x=315, y=0,width=135)

        self.btn_recherche = Button(self.frame_recherche,command=self.afficher, text="Tous",font=("times new roman",15,"bold"),bg="lightyellow", cursor="hand2")
        self.btn_recherche.place(x=470, y=0,width=135)
        
        self.btn_recherche = Button(self.frame_recherche,command=self.imprimer, text="Imprimer",font=("times new roman",15,"bold"),bg="lightgray", cursor="hand2")
        self.btn_recherche.place(x=650, y=0,width=135)

        
        # Zone affichage facture
        self.frame_affiche_facture = Frame(self.frame_affichage, bd=2, bg="white", relief=RAISED)
        self.frame_affiche_facture.place(x=410, y=205, width=375, height=290)
        
        ctitre = Label(self.frame_affiche_facture, text="Zone facture du client",font=("goudy olf style",20,"bold"),bg="#f44336", bd=3).pack(side=TOP, fill=Y)

        scroll_y = Scrollbar(self.frame_affiche_facture, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = Scrollbar(self.frame_affiche_facture, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.txt_facture = Text(self.frame_affiche_facture, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.txt_facture.pack(fill=BOTH, expand=1)

        scroll_x.config(command=self.txt_facture.xview)
        scroll_y.config(command=self.txt_facture.yview)
        
        # Zone affichage facture
        self.frame_affiche_tableau = Frame(self.frame_affichage, bd=2, bg=background, relief=RAISED)
        self.frame_affiche_tableau.place(x=0, y=205, width=400, height=290)
         
          #liste
        scroll_y = Scrollbar(self.frame_affiche_tableau, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(self.frame_affiche_tableau, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.reserveliste = ttk.Treeview(self.frame_affiche_tableau, columns=("Id","Mobile","Date_debut","Date_fin","Type_salle","Nom_salle","Nombre_place","Type_activite","Prix_salle","Nombre_jour","Total_payer"), yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
        
        scroll_x.config(command=self.reserveliste.xview)
        scroll_y.config(command=self.reserveliste.yview)

        self.reserveliste.heading("Id", text="ID", anchor="w")
        self.reserveliste.heading("Mobile", text="Mobile",anchor="w")
        self.reserveliste.heading("Date_debut", text="Date_debut",anchor="w")
        self.reserveliste.heading("Date_fin", text="Date_fin",anchor="w")
        self.reserveliste.heading("Type_salle", text="Type_salle",anchor="w")
        self.reserveliste.heading("Nom_salle", text="Nom_salle",anchor="w")
        self.reserveliste.heading("Nombre_place", text="Nombre_place",anchor="w")
        self.reserveliste.heading("Type_activite", text="Type_activite",anchor="w")
        self.reserveliste.heading("Prix_salle", text="Prix_salle",anchor="w")
        self.reserveliste.heading("Nombre_jour", text="Nombre_jour",anchor="w")
        self.reserveliste.heading("Total_payer", text="Total_payer",anchor="w")
        
        self.reserveliste["show"]="headings" 
        self.reserveliste.pack(fill=BOTH, expand=1)

        self.reserveliste.bind("<ButtonRelease-1>", self.obtenir_information)

        self.afficher()
        

    def listesalle(self):
        self.liste_salle.append("vide")
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            cur.execute("select nom from salle")
            salle = cur.fetchall()
            if len(salle)>0:
                del self.liste_salle[:]
                for i in salle:
                    self.liste_salle.append(i[0])

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")
            
    def verifie_identite(self):

        #### verification pour nom
        if self.var_mobile.get()=="":
            messagebox.showerror("Erreur", "Veillez saisir le numero du client ")
        else:
            con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
            cur = con.cursor()
            cur.execute("select Nom from client where Mobile=?", (self.var_mobile.get(),))
            self.var_nom = cur.fetchone()
            if self.var_nom == None:
                messagebox.showerror("erreur","Le client n'est pas enregistrer")
            else:
                con.commit()
                con.close()
                lbl_nom = Label(self.frame_affiche_identite, text="Nom :",font=("times new roman",18,"bold"),bg="cyan").place(x=0, y=0)
                self.nom = Label(self.frame_affiche_identite, text=self.var_nom,font=("times new roman",18), bg="cyan")
                self.nom.place(x=100, y=0, width=100)

            

        #### verification pour Prenom
        if self.var_mobile.get()=="":
            messagebox.showerror("Erreur", "Veillez saisir le numero du client ")
        else:
            con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
            cur = con.cursor()
            cur.execute("select Prenom from client where Mobile=?", (self.var_mobile.get(),))
            self.var_prenom = cur.fetchone()
            if self.var_prenom == None:
                messagebox.showerror("erreur","Le client n'est pas enregistrer")
            else:
                con.commit()
                con.close()
                lbl_prenom = Label(self.frame_affiche_identite, text="Prenom :",font=("times new roman",18,"bold"),bg="cyan").place(x=0, y=30)
                self.prennom = Label(self.frame_affiche_identite, text=self.var_prenom,font=("times new roman",18), bg="cyan")
                self.prennom.place(x=100, y=30, width=100)


         #### verification pour Pays
        if self.var_mobile.get()=="":
            messagebox.showerror("Erreur", "Veillez saisir le numero du client ")
        else:
            con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
            cur = con.cursor()
            cur.execute("select Pays from client where Mobile=?", (self.var_mobile.get(),))
            self.var_pays = cur.fetchone()
            if self.var_pays == None:
                messagebox.showerror("erreur","Le client n'est pas enregistrer")
            else:
                con.commit()
                con.close()
                lbl_pays = Label(self.frame_affiche_identite, text="Pays :",font=("times new roman",18,"bold"),bg="cyan").place(x=0, y=60)
                self.pays = Label(self.frame_affiche_identite, text=self.var_pays,font=("times new roman",18), bg="cyan")
                self.pays.place(x=100, y=60, width=100)
    

         #### verification pour type identite
        if self.var_mobile.get()=="":
            messagebox.showerror("Erreur", "Veillez saisir le numero du client ")
        else:
            con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
            cur = con.cursor()
            cur.execute("select Type_Identite from client where Mobile=?", (self.var_mobile.get(),))
            self.var_type_identite = cur.fetchone()
            if self.var_type_identite == None:
                messagebox.showerror("erreur","Le client n'est pas enregistrer")
            else:
                con.commit()
                con.close()
                lbl_type_identite = Label(self.frame_affiche_identite, text="Type_Identite :",font=("times new roman",18,"bold"),bg="cyan").place(x=250, y=0)
                self.typeIdentite = Label(self.frame_affiche_identite, text=self.var_type_identite,font=("times new roman",18), bg="cyan")
                self.typeIdentite.place(x=410, y=0, width=170)
    

         #### verification pour numero identite
        if self.var_mobile.get()=="":
            messagebox.showerror("Erreur", "Veillez saisir le numero du client ")
        else:
            con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
            cur = con.cursor()
            cur.execute("select Numero_Identite from client where Mobile=?", (self.var_mobile.get(),))
            self.var_num_identite = cur.fetchone()
            if self.var_num_identite == None:
                messagebox.showerror("erreur","Le client n'est pas enregistrer")
            else:
                con.commit()
                con.close()
                lbl_num_identite = Label(self.frame_affiche_identite, text="Numero Identite :",font=("times new roman",18,"bold"),bg="cyan").place(x=250, y=30)
                self.numIdentite = Label(self.frame_affiche_identite, text=self.var_num_identite,font=("times new roman",18), bg="cyan")
                self.numIdentite.place(x=410, y=30, width=170)


         #### verification pour Adresse 
        if self.var_mobile.get()=="":
            messagebox.showerror("Erreur", "Veillez saisir le numero du client ")
        else:
            con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
            cur = con.cursor()
            cur.execute("select Adresse from client where Mobile=?", (self.var_mobile.get(),))
            self.var_adresse = cur.fetchone()
            if self.var_adresse == None:
                messagebox.showerror("erreur","Le client n'est pas enregistrer")
            else:
                con.commit()
                con.close()
                lbl_adressse = Label(self.frame_affiche_identite, text="Adresse :",font=("times new roman",18,"bold"),bg="cyan").place(x=250, y=60)
                self.adressse = Label(self.frame_affiche_identite, text=self.var_adresse,font=("times new roman",18), bg="cyan")
                self.adressse.place(x=410, y=60, width=170)
    
    def facture(self):
        date_debut = self.var_date_debut.get_date()
        date_fin = self.var_date_fin.get_date()
        if date_debut == date_fin :
            messagebox.showerror("erreur","la date du debut doit etre different du date de fin.")
        else:
            delta = date_fin - date_debut
            self.var_nombre_jour = delta.days
            nombre_jour = self.var_nombre_jour
            prix_salle = int(self.var_prix_salle.get())
            total_a_payer = prix_salle * nombre_jour 

            tt = str(total_a_payer)

            self.txt_nombre_jour.config(text=f"{self.var_nombre_jour}")
            # print(self.var_nombre_jour)
            self.var_total_a_payer.set(tt)

    def reservation(self):
        date_debut = self.var_date_debut.get_date()
        date_fin = self.var_date_fin.get_date()
        nombre_jour = str(self.var_nombre_jour)
        if self.var_mobile.get()=="":
            messagebox.showerror("Erreru", "Veillez saisir le numero mobile")

        elif self.var_nombre_jour < 0 :
            messagebox.showerror("Erreru", "La date de debut ne doit pas etre inferieur a la date de fin.")
       
        elif date_debut == date_fin : 
            messagebox.showerror("Erreur","La date de debut doit etre different a la date du fin.")
        else:
            try:
                con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
                cur = con.cursor()
                cur.execute("Select count(*) from reservation where Nom_salle=? AND ( (Date_debut<=? AND Date_fin>=?) OR (Date_debut<=? AND Date_fin>=?))",
                (self.var_nom_salle.get(), date_fin, date_debut, date_debut, date_fin))
                count = cur.fetchone()[0]
                if count==0:
                    cur.execute("insert into reservation(Mobile,Date_debut,Date_fin,Type_salle,Nom_salle,Nombre_place,Type_activite,Prix_salle,Nombre_jour,Total_payer) values(?,?,?,?,?,?,?,?,?,?)",(
                    self.var_mobile.get(),
                    date_debut,
                    date_fin,
                    self.var_type_salle.get(),
                    self.var_nom_salle.get(),
                    self.var_nombre_place.get(),
                    self.var_type_activite.get(),
                    self.var_prix_salle.get(),
                    nombre_jour,
                    self.var_total_a_payer.get()

                    ))
                    con.commit()
                    con.close()
                    self.afficher()
                    self.reinitiliser()
                    self.generer_facture()
                    messagebox.showinfo("Success","Reservation efffectuee avec success")
                else:
                    messagebox.showerror("Erreur", "La date est reserver entrez une autre date.")

            except Exception as ex:
                messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    def afficher(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            cur.execute("select * from reservation")
            rows = cur.fetchall()
            self.reserveliste.delete(*self.reserveliste.get_children())
            for row in rows:
                self.reserveliste.insert("",END, values=row)
           
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion  {str(ex)}")
           

    def obtenir_information(self, ev):
        self.btn_ajouter.config(state=DISABLED)
        self.btn_modifier.config(state=NORMAL)
        self.btn_annuler.config(state=NORMAL)

        r = self.reserveliste.focus()
        contenu = self.reserveliste.item(r)
        row = contenu["values"]

        self.var_id.set(row[0])
        self.var_mobile.set(row[1])

        date_str = row[2]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date_inverse = datetime.strftime(date_obj, "%d/%m/%Y")
        self.var_date_debut.set_date(date_inverse)

        date_str1 = row[3]
        date_obj1 = datetime.strptime(date_str1, "%Y-%m-%d")
        date_inverse1 = datetime.strftime(date_obj1, "%d/%m/%Y")
        self.var_date_fin.set_date(date_inverse1)

        delta = date_obj1 - date_obj

        self.var_nombre_jour = delta.days

        self.var_type_salle.set(row[4])
        self.var_nom_salle.set(row[5])
        self.var_nombre_place.set(row[6])
        self.var_type_activite.set(row[7])
        self.var_prix_salle.set(row[8])
        self.txt_nombre_jour.config(text=f"{self.var_nombre_jour}")
        self.var_total_a_payer.set(row[10])

    def modifier(self):
        date_debut = self.var_date_debut.get_date()
        date_fin = self.var_date_fin.get_date()
        nombre_jour = str(self.var_nombre_jour)
        if self.var_mobile.get()=="":         
            messagebox.showerror("Erreru", "Veillez saisir le numero mobile")

        elif self.var_nombre_jour < 0 :
            messagebox.showerror("Erreru", "La date de debut ne doit pas etre inferieur a la date de fin.")
       
        else:
            try:
                con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
                cur = con.cursor()
                cur.execute("Select count(*) from reservation where Nom_salle=? AND ( (Date_debut<=? AND Date_fin>=?) OR (Date_debut<=? AND Date_fin>=?))",
                (self.var_nom_salle.get(), date_fin, date_debut, date_debut, date_fin))
                count = cur.fetchone()[0]
                if count==0:
                    cur.execute("update reservation set Mobile=?, Date_debut=?, Date_fin=?, Type_salle=?, Nom_salle=?, Nombre_place=?, Type_activite=?, Prix_salle=?, Nombre_jour=?, Total_payer=? where Id=? ",(
                    self.var_mobile.get(),
                    date_debut,
                    date_fin,
                    self.var_type_salle.get(),
                    self.var_nom_salle.get(),
                    self.var_nombre_place.get(),
                    self.var_type_activite.get(),
                    self.var_prix_salle.get(),
                    nombre_jour,
                    self.var_total_a_payer.get(),
                    self.var_id.get()
                    ))
                    con.commit()
                    con.close()
                    self.afficher()
                    self.generer_facture()
                    messagebox.showinfo("Success","Reservation modifier effectuee avec success")
                else:
                    messagebox.showerror("Erreur","la date est deja reservee")

            except Exception as ex:
                messagebox.showerror("Erreur",f"Erreur de connexion  {str(ex)}")
            


    def supprimer(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            op = messagebox.askyesno("Confirmer","Voulez-vous vraiment annuler cette reservation ")
            if op ==True:
                cur.execute("delete from reservation where Id=?",(self.var_id.get(),))
                con.commit()
                con.close()
                self.afficher()
                self.reinitiliser()
                messagebox.showinfo("Supprimer", "Resevation annuler avec success!")

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion  {str(ex)}")
    

    def generer_facture(self):
  #      if self.var_mobile.get()=="":
  #          messagebox.showerror("Erreur","Veillez saisir le numero du client")
   #     else:
        
        self.entete_facture()

        self.footer_facture()

        fp = open(fr"C:/Users/hp 8470p/Desktop/Reservation_en_Python/Reservation/facture{str(self.facture)}.txt", "w")
        fp.write(self.txt_facture.get("1.0", END))
        fp.close
        messagebox.showinfo("Sauvergarder","Enregistrement éffectué avec succés")
        self.ck_print = 1


    def entete_facture(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()

        cur.execute("select Nom from client where Mobile=?",(self.var_mobile.get(),))
        self.var_nom_client = cur.fetchone()
        con.commit()
        con.close()

        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()

        cur.execute("select Prenom from client where Mobile=?",(self.var_mobile.get(),))
        self.var_prenom_client = cur.fetchone()
        con.commit()
        con.close()

        self.facture = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))

        facture_entet = f'''
        Reservation de salle 
        {str("="*37)}
        Nom du client : {self.var_nom_client}
        Prenom du client :{self.var_prenom_client}
        Telephone : {self.var_mobile.get()}
        Numero facture : {str(self.facture)}
        Date : {str(time.strftime("%d%m%Y"))}
        {str("="*37)}
        '''

        self.txt_facture.delete("1.0",END)
        self.txt_facture.insert("1.0", facture_entet)

    def footer_facture(self):
        facture_foot = f'''

        {str("="*37)}
        Date debut : {self.var_date_debut.get()}
        Date fin : {self.var_date_fin.get()}
        Nom salle : {self.var_nom_salle.get()}
        Somme totale : {self.var_total_a_payer.get()}
        {str("="*37)}

        ''' 
   
        self.txt_facture.insert(END, facture_foot)

    def imprimer(self):
        if self.ck_print == 1:
            messagebox.showinfo("Impression", "Impression en cours")
            fichier = tempfile.mktemp(".txt")
            open(fichier,"w").write(self.txt_facture.get("1.0",END))
            os.startfile(fichier,"print")
        else:
            messagebox.showerror("Erreur", "Veillez generer la facture dabord")

    def recherche(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            if self.var_recherche.get()=="":
                messagebox.showerror("Erreur","Entrer votre recherhce")
            else:
                cur.execute("select * from reservation where "+self.var_type_recherche.get()+" LIKE '%"+self.var_recherche.get()+"%'")
                row = cur.fetchall()    
                if len(row) != 0:
                    self.reserveliste.delete(*self.reserveliste.get_children())
                    for rows in row:
                        self.reserveliste.insert("",END, values=rows)
                else:
                    messagebox.showerror("erreur","Aucun trouve ")
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

    def reinitiliser(self):
        self.btn_ajouter.config(state=NORMAL)
        self.btn_modifier.config(state=DISABLED)
        self.btn_annuler.config(state=DISABLED)

        self.var_mobile.set("")
        self.var_type_salle.set("")
        self.var_nom_salle.set("Choisir votre salle")
        self.var_nombre_place.set("")
        self.var_type_activite.set("")
        self.var_prix_salle.set("")
        self.txt_nombre_jour.config(text="")
        self.var_total_a_payer.set("")


if __name__ =="__main__":
    root = Tk()
    obj = Reservation(root)
    root.mainloop()
