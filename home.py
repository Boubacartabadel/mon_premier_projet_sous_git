from tkinter import *
from tkinter import ttk, messagebox
#from PIL import Image, ImageTK
import time
import sqlite3
import os


class Home:
    def __init__(self,root):
        background = "cyan"
        self.root = root
        self.root.title("Homme")
        self.root.geometry("1200x700+0+0")
        self.root.config(bg=background)

        client =  Button(self.root, text="Client",command=self.page_client, font=("times new roman",12,"bold"), bd=0, activebackground=background, bg=background, cursor="hand2").place(x=10, y=10)
        reservation =  Button(self.root, text="Reservation", command=self.page_reservation, font=("times new roman",12,"bold"), bd=0, activebackground=background, bg=background, cursor="hand2").place(x=100, y=10)
        plainte =  Button(self.root, text="Plainte",command=self.page_plainte, font=("times new roman",12,"bold"), bd=0, activebackground=background, bg=background, cursor="hand2").place(x=230, y=10)

        deconnecter =  Button(self.root, text="Deconnecter",command=self.deconnecte, font=("times new roman",12,"bold"), bd=0, activebackground=background,bg="red", cursor="hand2").place(x=1250, y=10)
        
        self.frame_main = Frame(self.root, bd=4, relief= RAISED, width=1186, height=650)
        self.frame_main.place(x=10, y=45)

        self.lbl_heure = Label(self.root, text="",font=("times new roman",12,"bold"), bg="black", fg="white")
        self.lbl_heure.place(x=0, y=70, relwidth=1, height=40)

###### cadre 1

        self.corp2 = Frame(self.frame_main, bg="#009aa5")
        self.corp2.place(x=10, y=200, width=310, height=220)

        #self.totalclientImage = Image.open("chemin d'acces a l'image")
        #photo = Image.ImageTK(self.totalclientImage)

        #self.totalclient = Label(self.corp2, image=photo, bg="#009aa5")

        #self.totalclient.image = photo
        #self.totalclient.place(x=220, y=0)

        self.ntotalclient_text = Label(self.corp2, text="0", bg="#009aa5", font=("times new roman",25,"bold"), bd=0)
        self.ntotalclient_text.place(x=120, y=100)

        self.totalclient_text = Label(self.corp2, text="Total client", bg="#009aa5", font=("times new roman",25,"bold"), bd=0)
        self.totalclient_text.place(x=5, y=5)

###### cadre 2

        self.corp3 = Frame(self.frame_main, bg="#e21f26")
        self.corp3.place(x=400, y=200, width=310, height=220)

        #self.totalemployeImage = Image.open("C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation")
        #photo = Image.ImageTK(self.totalemployeImage)

        #self.totalemploye = Label(self.corp3, image=photo, bg="#e21f26")

        #self.totalemploye.image = photo
        #self.totalemploye.place(x=220, y=0)

        self.ntotalemploye_text = Label(self.corp3, text="0", bg="#e21f26", font=("times new roman",25,"bold"), bd=0)
        self.ntotalemploye_text.place(x=120, y=100)

        self.totalemploye_text = Label(self.corp3, text="Total Employe", bg="#e21f26", font=("times new roman",25,"bold"), bd=0)
        self.totalemploye_text.place(x=5, y=5)

###### cadre 3

        self.corp4 = Frame(self.frame_main, bg="#ffcb1f")
        self.corp4.place(x=800, y=200, width=310, height=220)

        #self.totalventeImage = Image.open("chemin d'acces a l'image")
        #photo = Image.ImageTK(self.totalventeImage)

        #self.totalvente = Label(self.corp3, image=photo, bg="#ffcb1f")

        #self.totalvente.image = photo
        #self.totalvente.place(x=220, y=0)

        self.ntotalvente_text = Label(self.corp4, text="0", bg="#ffcb1f", font=("times new roman",25,"bold"), bd=0)
        self.ntotalvente_text.place(x=120, y=100)

        self.totalvente_text = Label(self.corp4, text="Total Vente", bg="#ffcb1f", font=("times new roman",25,"bold"), bd=0)
        self.totalvente_text.place(x=5, y=5)
        
        self.modifier_contenu()

        heure_ = (time.strftime("%H:%M:%S"))
        date_ = (time.strftime("%d-%m-%Y"))
        self.lbl_heure.config(text=f"Bienvenue chez Hourr@ Reservation \t\t Date: {str(date_)} \t\t Heure: {str(heure_)}")
        self.lbl_heure.after(200, self.modifier_contenu)

    def page_client(self):
        self.root1 = Toplevel(self.root)
        self.root1.title("Page Client")
        self.root1.geometry("1000x700+100+100")


        self.root1.mainloop()
       

    def page_plainte(self):
        self.root2 = Toplevel(self.root)
        self.root2.title("Page Plainte")
        self.root2.geometry("1000x700+100+100")


        self.root2.mainloop()
     

    def page_reservation(self):
        self.root3 = Toplevel(self.root)
        self.root3.title("Page reservation")
        self.root3.geometry("1000x700+100+100")


        self.root3.mainloop()
    def deconnecte(self):
        self.root4.destroy
        self.root4 = Toplevel(self.root)
        self.root4.title("Page client")
        self.root4.geometry("1000x700+100+100")


        self.root4.mainloop()

        


    def modifier_contenu(self):
        con = sqlite3.connect(database=r"C:\Users\hp 8470p\Desktop\Reservation_en_Python\Reservation\reservationbase.db")
        cur = con.cursor()
        try:
            cur.execute("select * from client")
            client = cur.fetchall()
            self.ntotalclient_text.config(text=f"{str(len(client))}")

            cur.execute("select * from admin")
            admin = cur.fetchall()
            self.ntotalemploye_text.config(text=f"{str(len(admin))}") 

            cur.execute("select sum(Total_payer) from reservation")
            total = cur.fetchall()
            self.ntotalvente_text.config(text=total)
            
        except Exception as ex:
            messagebox.showerror("erreur",f"Erreur de connexion {str(ex)}")








if __name__ =="__main__":
    root = Tk()
    obj = Home(root)
    root.mainloop()


