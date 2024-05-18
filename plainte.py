from tkinter import *
from tkinter import ttk, messagebox
#from PIL import Image, ImageTK
import time
import sqlite3
import os


class Plainte:
    def __init__(self,root):
        background = "cyan"
        self.root = root
        self.root.title("Plainte")
        self.root.geometry("1200x580+70+70")
        self.root.config(bg=background)

        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS plainte(Id INTEGER PRIMARY KEY AUTOINCREMENT, Nom text, Prenom text, Type_salle text, Nom_alle text, Probleme text, Budget text)")
        con.commit()
        con.close()

        self.liste_salle = []
        self.listesalle()

        self.var_id = StringVar()
        self.var_prenom_client = StringVar()
        self.var_nom_client = StringVar()
        self.var_type_salle = StringVar()
        self.var_nom_salle = StringVar()
        self.var_probleme = StringVar()
        self.var_budget = StringVar()

        self.var_type_recherche = StringVar()
        self.var_recherche = StringVar()

        self.plainte = LabelFrame(self.root, text="Administration",font=("times new roman",15,"bold"),bg=background,bd=4, relief=GROOVE, width=1188, height=575)
        self.plainte.place(x=5, y=0)
        
        # zone de saisi
        self.frame_saisi = Frame(self.plainte,bd=3, relief=RAISED,bg=background, width=800, height=200)
        self.frame_saisi.place(x=0, y=0)

        #labels
        lbl_nom_client = Label(self.frame_saisi, text="Nom client", font=("times new roman",20,"bold"),bg=background).place(x=60,y=0)
        txt_nom_client = ttk.Entry(self.frame_saisi,textvariable=self.var_nom_client ,font=("times new roman",20,"bold")).place(x=20,y=40, width=200, height=35)

        lbl_type_salle = Label(self.frame_saisi, text="Type salle", font=("times new roman",20,"bold"),bg=background).place(x=330,y=0)
        txt_type_salle = ttk.Entry(self.frame_saisi,textvariable=self.var_type_salle,font=("times new roman",20,"bold")).place(x=300,y=40, width=200,height=35)

        lbl_probleme = Label(self.frame_saisi, text="Probleme", font=("times new roman",20,"bold"),bg=background).place(x=560,y=0)
        txt_probleme = ttk.Entry(self.frame_saisi,textvariable=self.var_probleme , font=("times new roman",20,"bold")).place(x=540,y=40, width=200,height=35)

        lbl_prenom_client = Label(self.frame_saisi, text="Prenom", font=("times new roman",20,"bold"),bg=background).place(x=60,y=80)
        txt_prenom_client = ttk.Entry(self.frame_saisi,textvariable=self.var_prenom_client, font=("times new roman",20,"bold")).place(x=20,y=120, width=200)

        lbl_budget = Label(self.frame_saisi, text="Budget", font=("times new roman",20,"bold"),bg=background).place(x=560,y=80) 
        txt_budget = ttk.Entry(self.frame_saisi,textvariable=self.var_budget, font=("times new roman",20,"bold")).place(x=540, y=120,  width=200,height=35) 

        lbl_nom_salle = Label(self.frame_saisi, text="Nom_salle", font=("times new roman",20,"bold"),bg=background).place(x=330,y=80)
        txt_nom_salle = ttk.Combobox(self.frame_saisi,textvariable=self.var_nom_salle, font=("times new roman",20,"bold"), values=["Salle 1","Salle 2"], justify=CENTER, state="r")
        txt_nom_salle.current(0)
        txt_nom_salle.place(x=300,y=120, width=200)  


        # zone boutton 
        self.frame_bouton = Frame(self.plainte, bd=2, bg=background, relief=RAISED, width=355, height=200)
        self.frame_bouton.place(x=820, y=0)

        # btn
        self.btn_ajouter = Button(self.frame_bouton,command=self.ajouter ,text="Ajouter",font=("times new roman",15,"bold"),bg="green", cursor="hand2")
        self.btn_ajouter.place(x=0, y=0,width=150)

        self.btn_modifier = Button(self.frame_bouton,command=self.modifier,text="Modifier",font=("times new roman",15,"bold"),state=DISABLED,bg="yellow", cursor="hand2")
        self.btn_modifier.place(x=0,y=50,width=150)

        self.btn_supprimer = Button(self.frame_bouton,command=self.supprimer, text="Supprimer",font=("times new roman",15,"bold"),state=DISABLED,bg="red", cursor="hand2")
        self.btn_supprimer.place(x=0, y=100,width=150)

        self.btn_reinitiliser = Button(self.frame_bouton,command=self.reinitiliser, text="Reinitiliser",font=("times new roman",15,"bold"),bg="gray", cursor="hand2")
        self.btn_reinitiliser.place(x=0, y=150,width=150)

        type_recherche = ttk.Combobox(self.frame_bouton,textvariable=self.var_type_recherche,font=("times new roman",20,"bold"), values=["Type_salle","Nom_salle","Probleme"], justify=CENTER, state="r")
        type_recherche.current(0)
        type_recherche.place(x=160, y=0, width=170)

        recherche = ttk.Entry(self.frame_bouton, textvariable=self.var_recherche ,font=("times new roman",20,"bold")).place(x=160, y=50, width=170)

        self.btn_recherche = Button(self.frame_bouton,command=self.recherche, text="Recherche",font=("times new roman",15,"bold"),bg="lightgreen", cursor="hand2")
        self.btn_recherche.place(x=160, y=100,width=170)

        self.btn_tous = Button(self.frame_bouton,command=self.afficher ,text="Tous",font=("times new roman",15,"bold"),bg="lightyellow", cursor="hand2")
        self.btn_tous.place(x=160, y=150,width=170)


        # zone de la table
        self.frame_table = Frame(self.plainte, bd=3, bg=background, relief=RAISED)
        self.frame_table.place(x=0, y=205,relwidth=1, height=340)

        #liste
        scroll_y = Scrollbar(self.frame_table, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(self.frame_table, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.plainteliste = ttk.Treeview(self.frame_table, columns=("Id","Nom","Prenom","Type_salle","Nom_alle","Probleme","Budget"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
        
        scroll_x.config(command=self.plainteliste.xview)
        scroll_y.config(command=self.plainteliste.yview)

        self.plainteliste.heading("Id", text="ID", anchor="w")
        self.plainteliste.heading("Nom", text="Nom",anchor="w")
        self.plainteliste.heading("Prenom", text="Prenom",anchor="w")
        self.plainteliste.heading("Type_salle", text="Type_salle",anchor="w")
        self.plainteliste.heading("Nom_alle", text="Nom_alle",anchor="w")
        self.plainteliste.heading("Probleme", text="Probleme",anchor="w")
        self.plainteliste.heading("Budget", text="Budget",anchor="w")
        
        
        self.plainteliste["show"]="headings" 
        self.plainteliste.pack(fill=BOTH, expand=1)
        self.plainteliste.bind("<ButtonRelease-1>", self.obtenir_information)

        self.afficher()

    def ajouter(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:         
            cur.execute("insert into plainte(Nom , Prenom , Type_salle , Nom_alle, Probleme , Budget) values(?,?,?,?,?,?)",(
            self.var_prenom_client.get(),
            self.var_nom_client.get(),
            self.var_type_salle.get(),
            self.var_nom_salle.get(),
            self.var_probleme.get(),
            self.var_budget.get()
            ))
            con.commit()
            self.afficher()
            self.reinitiliser()
            con.close()
            messagebox.showinfo("Success","Enregistrement effectue avec success")
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion  {str(ex)}")
 
    def afficher(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            cur.execute("select * from plainte")
            rows = cur.fetchall()
            self.plainteliste.delete(*self.plainteliste.get_children())
            for row in rows:
                self.plainteliste.insert("",END, values=row)

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion  {str(ex)}")
    
   
      
    def obtenir_information(self, ev):
        self.btn_ajouter.config(state=DISABLED)
        self.btn_modifier.config(state=NORMAL)
        self.btn_supprimer.config(state=NORMAL)
        r = self.plainteliste.focus()
        contenu = self.plainteliste.item(r)
        row = contenu['values']  

        self.var_id.set(row[0]), 
        self.var_prenom_client.set(row[1]),
        self.var_nom_client.set(row[2]),
        self.var_type_salle.set(row[3]),
        self.var_nom_salle.set(row[4]),
        self.var_probleme.set(row[5]),
        self.var_budget.set(row[6])

    def reinitiliser(self):
        self.btn_ajouter.config(state=NORMAL)
        self.btn_modifier.config(state=DISABLED)
        self.btn_supprimer.config(state=DISABLED)

        self.var_id.set(""), 
        self.var_prenom_client.set(""),
        self.var_nom_client.set(""),
        self.var_type_salle.set(""),
        self.var_nom_salle.set("Salle 1"),
        self.var_probleme.set(""),
        self.var_budget.set(""),


    def modifier(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            cur.execute("update plainte set Nom=? , Prenom=? , Type_salle=? , Nom_alle=?, Probleme=? , Budget=? where Id=?",(              
                self.var_nom_client.get(), 
                self.var_prenom_client.get(),
                self.var_type_salle.get(),
                self.var_nom_salle.get(),
                self.var_probleme.get(),
                self.var_budget.get(),
                self.var_id.get()

                
            ))
            con.commit()
            self.afficher()
            self.reinitiliser()
            con.close()
            
            
            messagebox.showinfo("Success","Modification effectuer avec success!")

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion  {str(ex)}")

    def supprimer(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            op = messagebox.askyesno("Confirmer","Voulez-vous vraiment supprimer cette plainte")
            if op ==True:
                cur.execute("delete from plainte where Id=?",(self.var_id.get(),))
                con.commit()
                self.afficher()
                con.close()
               
                messagebox.showinfo("Supprimer", "Suppression effectue avec success!")

        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion  {str(ex)}")

   
    def recherche(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            if self.var_recherche.get()=="":
                messagebox.showinfo("Erreur","Veillez saisir votre recherche")
            else:
                cur.execute("select * from plainte where "+self.var_type_recherche.get()+" LIKE '%"+self.var_recherche.get()+"%'")
                row = cur.fetchall()
                if len(row)!=0:
                    self.plainteliste.delete(*self.plainteliste.get_children())
                    for rows in row:
                        self.plainteliste.insert("",END, values=rows)
                else:
                    messagebox.showerror("Erreur","Aucun trouvé")  
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")

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
            

         



if __name__ =="__main__":
    root = Tk()
    obj = Plainte(root)
    root.mainloop()
