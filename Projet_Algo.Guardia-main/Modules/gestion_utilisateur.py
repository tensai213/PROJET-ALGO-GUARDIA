import pandas as pnd
import hashlib
import os
import time

GREEN = "\033[1;32m"
RED = "\033[31m"
BLUE = "\033[94m"
END = "\033[0m"

def create_userfile():
    file_path = "./data/Utilisateurs.csv"
    if not os.path.exists(file_path):
        user_dataf = pnd.DataFrame(columns=["user_id", "nom", "mot_de_passe", "sel"])
        user_dataf.to_csv(file_path, index=False)
        print(f"{BLUE}Création de la Base de donnée utilisateur ...{END}\n")
        time.sleep(0.02)
        print(f"{GREEN}Base de donnée créée avec succès{END}\n{BLUE}Chargement du fichier 💾... !")
        print(f"{GREEN}-- Utilisateurs.csv --{END}\n")
    else:
        print(f"{GREEN}-- CREATION D'UTILISATEUR --{END}\n")
        user_dataf = pnd.read_csv(file_path)
        if "user_id" not in user_dataf.columns:
            print("Ajout de la colonne 'user_id'")
            user_dataf["user_id"] = range(1, len(user_dataf) + 1)
            save_users(user_dataf)


# Charger les utilisateurs depuis le fichier CSV
def load_users():
    try:
        return pnd.read_csv("./data/Utilisateurs.csv")
    except FileNotFoundError:
        return pnd.DataFrame(columns=["user_id", "nom", "mot_de_passe", "sel"])


# Sauvegarder les utilisateurs dans le fichier CSV
def save_users(dataf):
    dataf.to_csv("./data/Utilisateurs.csv", index=False)


# Charger les mots de passe compromis depuis rockyou-75.txt
def load_compromised_passwords(filepath="rockyou-75.txt"):
    """
    Charge les mots de passe compromis depuis un fichier texte.
    Chaque mot de passe doit être sur une nouvelle ligne.
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        print(f"{RED}Fichier {filepath} introuvable ! Assurez-vous qu'il est dans le bon dossier.{END}")
        return set()


# Hachage du mot de passe
def hash_mdp(mdp, salt=None):
    if not salt:
        salt = os.urandom(16)
    hash = hashlib.sha256(salt + mdp.encode("utf-8")).hexdigest()
    return hash, salt


# Ajouter un utilisateur
def add_users(nom, mdp):
    # Charger les mots de passe compromis
    compromised_passwords = load_compromised_passwords()

    # Vérifier si le mot de passe est compromis
    if mdp in compromised_passwords:
        print(f"\n{RED}Le mot de passe choisi est trop faible, car il fait partie d'une liste de mots de passe compromis.{END}")
        return

    users = load_users()
    if nom in users["nom"].values:
        print(f"\n{RED}Nom d'utilisateur déjà pris !{END}")
        return

    # Générer un user_id unique
    user_id = users["user_id"].max() + 1 if not users.empty else 1

    # Hacher le mot de passe
    hashed_mdp, salt = hash_mdp(mdp)

    # Ajouter l'utilisateur
    users = users._append({"user_id": user_id, "nom": nom, "mot_de_passe": hashed_mdp, "sel": salt}, ignore_index=True)
    save_users(users)
    print(f"{GREEN}Utilisateur ajouté avec succès !{END}")


# Supprimer un utilisateur
def supp_users(nom, mdp):
    dataf = load_users()
    dataf = dataf[dataf["nom"] != nom]
    save_users(dataf)



# --------------------------------------------------------------------------------------------------------------

#def db_mdp():
    file_path = "./data/mdp_compromis.csv"
    if not os.path.exists(file_path):
        mdp_dataf = pnd.DataFrame(columns=["mdp_compromis", "mdp_hasher"])
        mdp_dataf.to_csv(file_path, index=False)
        print("Base de donnée bien créée")
    else:
        print("-- mdp_compromis.csv --")
        mdp_dataf = pnd.read_csv(file_path)

        