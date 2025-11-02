import sqlite3 as sql
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk


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
        """Insérer une ligne. data doit être un dict {colonne: valeur}"""
        cols = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        self.cursor.execute(f'INSERT INTO {table} ({cols}) VALUES ({placeholders})', tuple(data.values()))
        self.conn.commit()

    def update(self, table, data, condition):
        """
        Met à jour une ligne.
        data: dict {colonne: nouvelle_valeur}
        condition: string SQL, exemple "id=1"
        """
        set_clause = ', '.join([f"{col} = ?" for col in data])
        self.cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {condition}", tuple(data.values()))
        self.conn.commit()

    def delete(self, table, condition):
        """Supprime les lignes correspondant à la condition"""
        self.cursor.execute(f"DELETE FROM {table} WHERE {condition}")
        self.conn.commit()

    def fetch_all(self, table):
        """Retourne toutes les lignes d'une table"""
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.cursor.fetchall()

    def add_column(self, table, column_name, column_type):
        """Ajoute une colonne à la table"""
        try:
            self.cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column_name} {column_type}")
            self.conn.commit()
        except sql.OperationalError:
            pass  # colonne existe déjà
class Adminpage:
    def __init__(self, username):
        self.db=DatabaseManager(username)
        self.db.create_table("etudiant", {"nom": "TEXT", "age": "INTEGER"})
        self.root=Toplevel()
        self.root.title("Table")
        self.root.geometry("600x400")
        Label(self.root, text=f"Bienvenue {username}", font=("Arial", 14)).pack(pady=10)
        Button(self.root, text="Afficher les étudiants", command=self.display).pack(pady=5)
        Button(self.root, text="Ajouter étudiant", command=self.add_student).pack(pady=5)
        Button(self.root,text="Ajouter une colonne",command=self.add_column).pack(pady=5)
        Button(self.root,text="Mise a jour",command=self.update_Button).pack(pady=5)
        Button(self.root,text="Quitter",command=self.root.destroy).pack(pady=5)



    def display(self):
        rows = self.db.fetch_all("etudiant")
        cols = self.get_columns()
        display_win = Toplevel(self.root)
        display_win.title("Liste des étudiants")

        tree = ttk.Treeview(display_win, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)

        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack(fill=BOTH, expand=True)

    def add_student(self):
        cols = self.get_columns()
        data = {}
        for col in cols:
            val = simpledialog.askstring(f"{col}", f"Entrez la valeur pour {col}")
            if val is None:  # annule
                return
            data[col] = val
        self.db.insert("etudiant", data)
        messagebox.showinfo("Succès", "Étudiant ajouté!")

    def add_column(self):
        col_name=simpledialog.askstring("Valeur","Nom de la colonne")
        col_type=simpledialog.askstring("Type","Type de la colonne")
        if col_name and col_type:
            self.db.add_column("etudiant", col_name, col_type)
            messagebox.showinfo("Succès", f"Colonne '{col_name}' ajoutée !")
    def get_columns(self):
        self.db.cursor.execute("PRAGMA table_info(etudiant)")
        return [info[1] for info in self.db.cursor.fetchall()]
    def mise_a_jour(self,col_name):
        rows=self.db.fetch_all("etudiant")
        if rows:
            for i,row in enumerate(rows):
                valeur=simpledialog.askfloat("Mise a jour",f"Entrez la valeur de '{col_name}' pour l'étudiant {i} ({row[0]}) :" )
                if valeur is not None:
                    # On récupère le nom ou l'identifiant pour faire la mise à jour
                    condition = f"nom='{row[0]}'"  # ici on se base sur le nom
                    self.db.update("etudiant", {col_name: valeur}, condition)
            messagebox.showinfo("Succès", f"Toutes les valeurs pour '{col_name}' ont été mises à jour !")

    def update_Button(self):
        cols=self.get_columns()
        if not cols:
            messagebox.showerror("Erreur", "Colonne n'existe pas")
            return
        col_name = simpledialog.askstring("Mise à jour", f"Quelle colonne souhaitez-vous modifier ?\n{cols}")
        if col_name not in cols:
            messagebox.showerror("Erreur", "Colonne invalide.")
            return
        self.mise_a_jour(col_name)