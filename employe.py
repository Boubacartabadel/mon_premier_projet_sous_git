from tkinter import *
from tkinter import ttk, messagebox
#from PIL import Image, ImageTK
import time
import sqlite3
import os


class Employe:
    def __init__(self,root):
        background = "cyan"
        self.root = root
        self.root.title("Employe")
        self.root.geometry("1200x580+70+70")
        self.root.config(bg=background)

        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS admin(Id INTEGER PRIMARY KEY ,Nom text,Prenom text,Login text,Role text,Password text)")
        con.commit()
        con.close()

        self.var_matricule = StringVar()
        self.var_prenom = StringVar()
        self.var_nom = StringVar()
        self.var_login = StringVar()
        self.var_password = StringVar()
        self.var_role = StringVar()
        self.var_type_recherche = StringVar()
        self.var_recherche = StringVar()
      
       


        self.administration = LabelFrame(self.root, text="Administration",font=("times new roman",15,"bold"),bg=background,bd=4, relief=GROOVE, width=1188, height=575)
        self.administration.place(x=5, y=0)
        
        # Zone de saisi information employe
        self.frame_saisi = Frame(self.administration,bd=3, relief=RAISED,bg=background, width=800, height=200)
        self.frame_saisi.place(x=0, y=0)

        lbl_matricule = Label(self.frame_saisi, text="Matricule", font=("times new roman",20,"bold"),bg=background).place(x=60,y=0)
        txt_matricule = ttk.Entry(self.frame_saisi,textvariable=self.var_matricule, font=("times new roman",20,"bold")).place(x=20,y=40, width=200, height=35)

        lbl_prenom = Label(self.frame_saisi, text="Prenom", font=("times new roman",20,"bold"),bg=background).place(x=330,y=0)
        txt_prenom = ttk.Entry(self.frame_saisi,textvariable=self.var_prenom,font=("times new roman",20,"bold")).place(x=300,y=40, width=200,height=35)

        lbl_motdepass = Label(self.frame_saisi, text="Mot de pass", font=("times new roman",20,"bold"),bg=background).place(x=560,y=0)
        txt_motdepass = ttk.Entry(self.frame_saisi,show=["*"],textvariable=self.var_password, font=("times new roman",20,"bold")).place(x=540,y=40, width=200,height=35)

        lbl_nom = Label(self.frame_saisi, text="Nom", font=("times new roman",20,"bold"),bg=background).place(x=60,y=80)
        txt_nom = ttk.Entry(self.frame_saisi,textvariable=self.var_nom, font=("times new roman",20,"bold")).place(x=20,y=120, width=200)

        lbl_login = Label(self.frame_saisi, text="Login", font=("times new roman",20,"bold"),bg=background).place(x=330,y=80)
        txt_login = ttk.Entry(self.frame_saisi,textvariable=self.var_login, font=("times new roman",20,"bold")).place(x=300,y=120, width=200)

        lbl_role = Label(self.frame_saisi, text="Role", font=("times new roman",20,"bold"),bg=background).place(x=560,y=80)
        txt_role = ttk.Combobox(self.frame_saisi,textvariable=self.var_role,font=("times new roman",20,"bold"), values=["Admin","Personnel"], justify=CENTER, state="r")
        txt_role.current(0)
        txt_role.place(x=540, y=120,  width=200,height=35)

        
        #Zone boutton 
        self.frame_bouton = Frame(self.administration, bd=2, bg=background, relief=RAISED, width=355, height=200)
        self.frame_bouton.place(x=820, y=0)
        # btn
        self.btn_ajouter = Button(self.frame_bouton,command=self.ajouter, text="Ajouter",font=("times new roman",15,"bold"),bg="green", cursor="hand2")
        self.btn_ajouter.place(x=0, y=0,width=150)

        self.btn_modifier = Button(self.frame_bouton,command=self.modifier, text="Modifier",font=("times new roman",15,"bold"),state=DISABLED,bg="yellow", cursor="hand2")
        self.btn_modifier.place(x=0,y=50,width=150)

        self.btn_supprimer = Button(self.frame_bouton,command=self.supprimer, text="Supprimer",font=("times new roman",15,"bold"),state=DISABLED,bg="red", cursor="hand2")
        self.btn_supprimer.place(x=0, y=100,width=150)

        self.btn_reinitiliser = Button(self.frame_bouton,command=self.reinitiliser, text="Reinitiliser",font=("times new roman",15,"bold"),bg="gray", cursor="hand2")
        self.btn_reinitiliser.place(x=0, y=150,width=150)

        type_recherche = ttk.Combobox(self.frame_bouton,textvariable=self.var_type_recherche,font=("times new roman",20,"bold"), values=["Nom","Prenom","Role","Login"], justify=CENTER, state="r")
        type_recherche.current(0)
        type_recherche.place(x=160, y=0, width=170)

        recherche = ttk.Entry(self.frame_bouton,textvariable=self.var_recherche,font=("times new roman",20,"bold")).place(x=160, y=50, width=170)

        self.btn_recherche = Button(self.frame_bouton,command=self.recherche, text="Recherche",font=("times new roman",15,"bold"),bg="lightgreen", cursor="hand2")
        self.btn_recherche.place(x=160, y=100,width=170)

        self.btn_tous = Button(self.frame_bouton,command=self.afficher, text="Tous",font=("times new roman",15,"bold"),bg="lightyellow", cursor="hand2")
        self.btn_tous.place(x=160, y=150,width=170)


        #Zone tableau 
        self.frame_table = Frame(self.administration, bd=3, bg=background, relief=RAISED)
        self.frame_table.place(x=0, y=205,relwidth=1, height=340)

        #liste
        scroll_y = Scrollbar(self.frame_table, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(self.frame_table, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.adminliste = ttk.Treeview(self.frame_table, columns=("Id","Nom","Prenom","Login","Role"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
        
        scroll_x.config(command=self.adminliste.xview)
        scroll_y.config(command=self.adminliste.yview)

        self.adminliste.heading("Id", text="Matricule", anchor="w")
        self.adminliste.heading("Nom", text="Nom",anchor="w")
        self.adminliste.heading("Prenom", text="Prenom",anchor="w")
        self.adminliste.heading("Login", text="Login",anchor="w")
        self.adminliste.heading("Role", text="Role",anchor="w")
        
        self.adminliste["show"]="headings" 
        self.adminliste.pack(fill=BOTH, expand=1)
        self.adminliste.bind("<ButtonRelease-1>", self.obtenir_information)

        self.afficher()


    def ajouter(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:  
            cur.execute("select * drom Admin where Login=?",(self.var_login.get(),))       
            ro = cur.fetchone()
            if ro !=None:
                messagebox.showerror("Erreur","User existe deja")
            cur.execute("insert into admin(Id, Nom, Prenom, Login, Role, Password) values(?,?,?,?,?,?)",(
            self.var_matricule.get(),
            self.var_prenom.get(),
            self.var_nom.get(),
            self.var_login.get(),
            self.var_role.get(),
            self.var_password.get()
            

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
            cur.execute("select * from admin")
            rows = cur.fetchall()
            self.adminliste.delete(*self.adminliste.get_children())
            for row in rows:
                self.adminliste.insert("",END, values=row)
           
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion  {str(ex)}")
                 
    def obtenir_information(self, ev):
        self.btn_ajouter.config(state=DISABLED)
        self.btn_modifier.config(state=NORMAL)
        self.btn_supprimer.config(state=NORMAL)
        r = self.adminliste.focus()
        contenu = self.adminliste.item(r)
        row = contenu['values']     
        self.var_matricule.set(row[0]),
        self.var_prenom.set(row[1]),
        self.var_nom.set(row[2]),
        self.var_login.set(row[3]),
        self.var_role.set(row[4]),
        self.var_password.set(row[5])

    def reinitiliser(self):
        self.btn_ajouter.config(state=NORMAL)
        self.btn_modifier.config(state=DISABLED)
        self.btn_supprimer.config(state=DISABLED)
        self.var_matricule.set(""),
        self.var_prenom.set(""),
        self.var_nom.set(""),
        self.var_login.set(""),
        self.var_role.set("Admin"),
        self.var_password.set("")

       

    def modifier(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            cur.execute("update admin set Nom=?, Prenom=?, Login=?, Role=?, Password=? where Id=?",(              
                self.var_nom.get(),
                self.var_prenom.get(),
                self.var_login.get(),
                self.var_role.get(),
                self.var_password.get(),
                self.var_matricule.get()
                
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
            op = messagebox.askyesno("Confirmer","Voulez-vous vraiment supprimer ce client")
            if op ==True:
                cur.execute("delete from admin where Id=?",(self.var_matricule.get(),))
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
                cur.execute("select * from admin where "+self.var_type_recherche.get()+" LIKE '%"+self.var_recherche.get()+"%'")
                row = cur.fetchall()
                if len(row)!=0:
                    self.adminliste.delete(*self.adminliste.get_children())
                    for rows in row:
                        self.adminliste.insert("",END, values=rows)
                else:
                    messagebox.showerror("Erreur","Aucun trouvé")  
        except Exception as ex:
            messagebox.showerror("Erreur",f"Erreur de connexion {str(ex)}")


if __name__ =="__main__":
    root = Tk()
    obj = Employe(root)
    root.mainloop()

