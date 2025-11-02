import sqlite3 as sql
from tkinter import *
from tkinter import messagebox, simpledialog, ttk


# ======================== CLASSE BASE DE DONNÉES ========================

class DatabaseManager:
    def __init__(self, db_name):
        """Initialise la connexion à la base"""
        self.conn = sql.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, name, columns_dict):
        """Créer une table si elle n'existe pas"""
        columns = ', '.join([f'{col} {dtype}' for col, dtype in columns_dict.items()])
        command = f"CREATE TABLE IF NOT EXISTS {name} ({columns})"
        self.cursor.execute(command)
        self.conn.commit()

    def insert(self, table, data):
        cols = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        self.cursor.execute(f'INSERT INTO {table} ({cols}) VALUES ({placeholders})', tuple(data.values()))
        self.conn.commit()

    def update(self, table, data, condition):
        set_clause = ', '.join([f"{col} = ?" for col in data])
        self.cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {condition}", tuple(data.values()))
        self.conn.commit()

    def delete(self, table, condition):
        self.cursor.execute(f"DELETE FROM {table} WHERE {condition}")
        self.conn.commit()

    def fetch_all(self, table):
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.cursor.fetchall()

    def add_column(self, table, column_name, column_type):
        try:
            self.cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column_name} {column_type}")
            self.conn.commit()
        except sql.OperationalError:
            pass

    def remove_column(self, table, column_name):
        """Supprime une colonne en recréant la table"""
        self.cursor.execute(f"PRAGMA table_info({table})")
        columns = [info[1] for info in self.cursor.fetchall() if info[1] != column_name]
        if len(columns) == 0:
            raise ValueError("Impossible de supprimer toutes les colonnes")
        cols_str = ', '.join(columns)
        tmp_table = f"{table}_tmp"
        # Créer une table temporaire
        self.cursor.execute(f"CREATE TABLE {tmp_table} AS SELECT {cols_str} FROM {table}")
        # Supprimer l'ancienne table
        self.cursor.execute(f"DROP TABLE {table}")
        # Renommer la table temporaire
        self.cursor.execute(f"ALTER TABLE {tmp_table} RENAME TO {table}")
        self.conn.commit()


# ======================== CLASSE ADMIN PAGE ========================

class Adminpage:
    def __init__(self, username):
        self.db = DatabaseManager(f"{username}.db")
        self.db.create_table("etudiant", {"nom": "TEXT", "age": "INTEGER"})

        self.root = Toplevel()
        self.root.title("Table des étudiants")
        self.root.geometry("650x450")
        self.root.configure(bg="#f0f0f0")

        Label(self.root, text=f"Bienvenue {username}", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        btn_params = {"width": 20, "font": ("Arial", 12), "bg": "#4CAF50", "fg": "white", "bd": 0, "activebackground": "#45a049"}

        Button(self.root, text="Afficher les étudiants", command=self.display, **btn_params).pack(pady=5)
        Button(self.root, text="Ajouter étudiant", command=self.add_student, **btn_params).pack(pady=5)
        Button(self.root, text="Ajouter une colonne", command=self.add_column, **btn_params).pack(pady=5)
        Button(self.root, text="Supprimer une colonne", command=self.delete_column, **btn_params).pack(pady=5)
        Button(self.root, text="Mise à jour", command=self.update_Button, **btn_params).pack(pady=5)
        Button(self.root, text="Supprimer étudiant", command=self.delete_student, **btn_params).pack(pady=5)
        Button(self.root, text="Quitter", command=self.root.destroy, **btn_params).pack(pady=10)

    def bring_to_front(self):
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after_idle(self.root.attributes, "-topmost", False)

    def display(self):
        rows = self.db.fetch_all("etudiant")
        cols = self.get_columns()
        display_win = Toplevel(self.root)
        display_win.title("Liste des étudiants")
        display_win.configure(bg="#f9f9f9")

        style = ttk.Style(display_win)
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#e6f2ff",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#e6f2ff",
                        font=("Arial", 12))
        style.map("Treeview", background=[("selected", "#3399ff")])

        tree = ttk.Treeview(display_win, columns=cols, show="headings")
        tree.tag_configure("oddrow", background="#ffffff")
        tree.tag_configure("evenrow", background="#cce6ff")

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)

        for i, row in enumerate(rows):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=row, tags=(tag,))

        tree.pack(fill=BOTH, expand=True)

    def add_student(self):
        self.bring_to_front()
        cols = self.get_columns()
        data = {}
        for col in cols:
            self.root.attributes("-topmost", True)
            val = simpledialog.askstring(f"{col}", f"Entrez la valeur pour {col}", parent=self.root)
            self.root.attributes("-topmost", False)
            if val is None:
                return
            data[col] = val
        self.db.insert("etudiant", data)
        messagebox.showinfo("Succès", "Étudiant ajouté !", parent=self.root)
        self.root.lift()

    def add_column(self):
        self.bring_to_front()
        self.root.attributes("-topmost", True)
        col_name = simpledialog.askstring("Nom", "Nom de la colonne :", parent=self.root)
        col_type = simpledialog.askstring("Type", "Type de la colonne :", parent=self.root)
        self.root.attributes("-topmost", False)
        if col_name and col_type:
            self.db.add_column("etudiant", col_name, col_type)
            messagebox.showinfo("Succès", f"Colonne '{col_name}' ajoutée !", parent=self.root)
        self.root.lift()

    def delete_column(self):
        self.bring_to_front()
        cols = self.get_columns()
        if not cols:
            messagebox.showinfo("Info", "Aucune colonne à supprimer", parent=self.root)
            return
        self.root.attributes("-topmost", True)
        col_name = simpledialog.askstring("Supprimer colonne", f"Nom de la colonne à supprimer :\n{cols}", parent=self.root)
        self.root.attributes("-topmost", False)
        if not col_name or col_name not in cols:
            messagebox.showerror("Erreur", "Colonne invalide", parent=self.root)
            return
        try:
            self.db.remove_column("etudiant", col_name)
            messagebox.showinfo("Succès", f"Colonne '{col_name}' supprimée !", parent=self.root)
        except ValueError as ve:
            messagebox.showerror("Erreur", str(ve), parent=self.root)
        self.root.lift()

    def get_columns(self):
        self.db.cursor.execute("PRAGMA table_info(etudiant)")
        return [info[1] for info in self.db.cursor.fetchall()]

    def mise_a_jour(self, col_name):
        self.bring_to_front()
        rows = self.db.fetch_all("etudiant")
        if rows:
            for i, row in enumerate(rows):
                self.root.attributes("-topmost", True)
                valeur = simpledialog.askstring("Mise à jour",
                                                f"Entrez la nouvelle valeur de '{col_name}' pour {row[0]} :",
                                                parent=self.root)
                self.root.attributes("-topmost", False)
                if valeur is not None:
                    condition = f"nom='{row[0]}'"
                    self.db.update("etudiant", {col_name: valeur}, condition)
            messagebox.showinfo("Succès", f"Les valeurs pour '{col_name}' ont été mises à jour !", parent=self.root)
        self.root.lift()

    def update_Button(self):
        self.bring_to_front()
        cols = self.get_columns()
        if not cols:
            messagebox.showerror("Erreur", "Aucune colonne trouvée.", parent=self.root)
            return
        col_name = simpledialog.askstring("Mise à jour", f"Quelle colonne souhaitez-vous modifier ?\n{cols}",
                                          parent=self.root)
        if col_name not in cols:
            messagebox.showerror("Erreur", "Colonne invalide.", parent=self.root)
            return
        self.mise_a_jour(col_name)

    def delete_student(self):
        self.bring_to_front()
        rows = self.db.fetch_all("etudiant")
        if not rows:
            messagebox.showinfo("Info", "Aucun étudiant à supprimer.", parent=self.root)
            return
        noms = [r[0] for r in rows if len(r) > 0]
        self.root.attributes("-topmost", True)
        nom = simpledialog.askstring("Suppression", f"Entrez le nom de l'étudiant à supprimer :\n{noms}", parent=self.root)
        self.root.attributes("-topmost", False)
        if not nom:
            return
        if nom not in noms:
            messagebox.showerror("Erreur", "Nom introuvable.", parent=self.root)
            return
        confirm = messagebox.askyesno("Confirmation", f"Supprimer l'étudiant '{nom}' ?", parent=self.root)
        if confirm:
            self.db.delete("etudiant", f"nom='{nom}'")
            messagebox.showinfo("Succès", f"Étudiant '{nom}' supprimé !", parent=self.root)
        self.root.lift()


# ======================== PAGE DE LOGIN ========================

conn = sql.connect("users.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS utilisateurs(user TEXT, password TEXT)")

fenetre = Tk()
fenetre.title("Login Page")
fenetre.geometry("300x150")
fenetre.configure(bg="#f0f0f0")

V1 = StringVar()
V2 = StringVar()

Label(fenetre, text="Utilisateur:", bg="#f0f0f0").grid(row=0, column=0)
Label(fenetre, text="Mot de passe:", bg="#f0f0f0").grid(row=1, column=0)

nom_entry = Entry(fenetre, textvariable=V1)
nom_entry.grid(row=0, column=1)
nom_entry.focus()

passwd_entry = Entry(fenetre, textvariable=V2, show="*")
passwd_entry.grid(row=1, column=1)

erreur_label = Label(fenetre, text="", bg="#f0f0f0")
erreur_label.grid(row=3, column=0, columnspan=2)


def login():
    user = V1.get().strip()
    pwd = V2.get().strip()
    if user == "" or pwd == "":
        erreur_label.config(text="Entrer le nom et le mot de passe", fg="red")
        return
    c.execute("SELECT * FROM utilisateurs WHERE user=? AND password=?", (user, pwd))
    if c.fetchone():
        fenetre.withdraw()
        Adminpage(user)
    else:
        erreur_label.config(text="Nom ou mot de passe incorrect", fg="red")


def creer_uti():
    user = V1.get().strip()
    passwd = V2.get().strip()
    if user == "" or passwd == "":
        erreur_label.config(text="Entrer le nom et le mot de passe", fg="red")
        return
    c.execute("SELECT * FROM utilisateurs WHERE user=?", (user,))
    if c.fetchone():
        erreur_label.config(text="Utilisateur déjà existant", fg="red")
        return
    c.execute("INSERT INTO utilisateurs(user,password) VALUES (?,?)", (user, passwd))
    conn.commit()
    db_user = DatabaseManager(f"{user}.db")
    db_user.create_table("etudiant", {"nom": "TEXT", "age": "INTEGER"})
    erreur_label.config(text=f"Utilisateur '{user}' créé avec succès", fg="green")
    V1.set("")
    V2.set("")
    nom_entry.focus()


Button(fenetre, text="Créer", command=creer_uti, width=10, bg="#2196F3", fg="white").grid(row=2, column=0)
Button(fenetre, text="Se connecter", command=login, width=10, bg="#4CAF50", fg="white").grid(row=2, column=1)

fenetre.mainloop()
