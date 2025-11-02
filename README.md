# Gestion des étudiants

Ce projet est une application Python pour **gérer une liste d'étudiants**.
Elle utilise **Tkinter** pour l'interface graphique et **SQLite** pour la base de données.

---

## Fonctionnalités

* Création et connexion d'utilisateurs.
* Ajouter, afficher, mettre à jour et supprimer des étudiants (CRUD complet).
* Ajouter et supprimer des colonnes dynamiquement.
* Interface graphique agréable avec couleurs et Treeview stylé.
* Support des bases SQLite individuelles par utilisateur.

---

## Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/ton_nom_utilisateur/nom_du_depot.git
```

2. Installer Python (>=3.8) si ce n’est pas déjà fait.
3. Installer les dépendances nécessaires (Tkinter est généralement inclus avec Python) :

```bash
pip install pillow
```

*(Si d'autres modules externes sont utilisés, liste-les ici.)*

---

## Utilisation

1. Lancer l'application :

```bash
python app.py
```

2. Créer un nouvel utilisateur ou se connecter avec un existant.
3. Utiliser les boutons pour gérer les étudiants :

* **Afficher les étudiants**
* **Ajouter étudiant**
* **Mise à jour**
* **Supprimer étudiant**
* **Ajouter colonne**
* **Supprimer colonne**

---

## Notes

* Chaque utilisateur possède sa propre base SQLite (`username.db`).
* La suppression de colonnes recrée la table sans supprimer les données restantes.
* Le Treeview utilise des couleurs alternées pour plus de lisibilité.

---

## Auteur

* **Karim** - Étudiant à **ENSAM Casablanca**
* Projet réalisé dans le cadre des études et pour apprentissage Python/Tkinter.
