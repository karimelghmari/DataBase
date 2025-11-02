from tkinter import *
import sqlite3 as sql
from database import DatabaseManager,Adminpage
conn=sql.connect("users.db")
c=conn.cursor()
c.execute("create table if not exists utilisateurs(user TEXT,password TEXT)")


fenetre = Tk()
fenetre.title("Login Page")
fenetre.geometry("300x150")

# Variables
V1 = StringVar()
V2 = StringVar()

# Labels et Entrées
Label(fenetre, text="Utilisateur:").grid(row=0, column=0)
Label(fenetre, text="Mot de passe:").grid(row=1, column=0)

nom_entry = Entry(fenetre, textvariable=V1)
nom_entry.grid(row=0, column=1)
nom_entry.focus()

passwd_entry = Entry(fenetre, textvariable=V2, show="*")
passwd_entry.grid(row=1, column=1)

# Label pour les erreurs
erreur_label = Label(fenetre, text="")
erreur_label.grid(row=3, column=0, columnspan=2)


# Fonction login
def login():
    user = V1.get().strip()
    pwd = V2.get().strip()
    if user=="" or pwd=="":
        erreur_label.config(text="Entrer le nom et le mot de passe", fg="red")
        return
    c.execute("SELECT * FROM utilisateurs WHERE user=? AND password=?",(user,pwd))
    if c.fetchone():
        fenetre.withdraw()  # cache la fenêtre login
        nouvelle_page(user)  # ouvre la page Admin
    else:
        erreur_label.config(text="Nom ou mot de passe incorrect", fg="red")


# Fonction nouvelle page
def nouvelle_page(user):
    Adminpage(user)
def creer_uti():
    user = V1.get().strip()
    passwd = V2.get().strip()
    if user=="" or passwd=="":
        erreur_label.config(text="Entrer le nom et le mot de passe", fg="red")
        return
    c.execute("SELECT * FROM utilisateurs WHERE user=?", (user,))
    if c.fetchone():
        erreur_label.config(text="Utilisateur déjà existant", fg="red")
        return
    c.execute("INSERT INTO utilisateurs(user,password) VALUES (?,?)",(user,passwd))
    conn.commit()
    # Crée automatiquement la base de l'utilisateur avec table étudiants
    db_user = DatabaseManager(f"{user}.db")
    db_user.create_table("etudiant", {"nom": "TEXT", "age": "INTEGER"})
    erreur_label.config(text=f"Utilisateur '{user}' créé avec succès", fg="green")
    V1.set("")
    V2.set("")
    nom_entry.focus()




# Boutons
create_B = Button(fenetre, text="Créer",command=creer_uti)
create_B.grid(row=2, column=0)

login_B = Button(fenetre, text="Se connecter", command=login)
login_B.grid(row=2, column=1)

fenetre.mainloop()
