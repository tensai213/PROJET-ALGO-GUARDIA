from Assets.br_charge import *
import pandas as pnd
import hashlib
import os
import time
from Modules.gestion_csv_produits import supp_produits_par_utilisateur

GREEN = "\033[1;32m"
RED = "\033[31m"
BLUE = "\033[94m"
END = "\033[0m"


def create_userfile():
    """
    Crée le fichier Utilisateurs.csv avec les colonnes nécessaires si celui-ci n'existe pas.
    """
    file_path = "./data/Utilisateurs.csv"
    if not os.path.exists(file_path):
        dataf = pnd.DataFrame(columns=["user_id", "nom", "mot_de_passe", "sel"])
        dataf.to_csv(file_path, index=False)
        print(f"{GREEN}Fichier Utilisateurs.csv créé avec succès !{END}")
    else:
        # Vérifier si les colonnes sont correctes
        dataf = load_users()
        if "user_id" not in dataf.columns:
            print(f"{RED}Correction du fichier Utilisateurs.csv : ajout de la colonne 'user_id'.{END}")
            dataf["user_id"] = range(1, len(dataf) + 1)
            save_users(dataf)
        print(f"{GREEN}Fichier Utilisateurs.csv déjà existant.{END}")

def load_users():
    try:
        return pnd.read_csv("./data/Utilisateurs.csv")
    except FileNotFoundError:
        return pnd.DataFrame(columns=["user_id", "nom", "mot_de_passe", "sel"])


def save_users(dataf):
    dataf.to_csv("./data/Utilisateurs.csv", index=False)


def hash_mdp(mdp, salt=None):
    if not salt:
        salt = os.urandom(16)
    return hashlib.sha256(salt + mdp.encode("utf-8")).hexdigest(), salt


def add_users(nom, mdp):
    users = load_users()
    if nom in users["nom"].values:
        print(f"{RED}Erreur : Nom d'utilisateur déjà pris !{END}")
        return

    user_id = users["user_id"].max() + 1 if not users.empty else 1
    hashed_mdp, salt = hash_mdp(mdp)
    users = users._append({"user_id": user_id, "nom": nom, "mot_de_passe": hashed_mdp, "sel": salt}, ignore_index=True)
    save_users(users)
    print(f"{GREEN}Utilisateur ajouté avec succès !{END}")


def login_user(nom, mdp):
    users = load_users()
    user = users[users["nom"] == nom]

    if user.empty:
        print(f"{RED}Utilisateur non trouvé.{END}")
        return False

    user = user.iloc[0]
    hashed_mdp, salt = user["mot_de_passe"], eval(user["sel"])
    if hash_mdp(mdp, salt)[0] == hashed_mdp:
        print(f"{GREEN}Connexion réussie !{END}")
        return user["user_id"]
    else:
        print(f"{RED}Mot de passe ou nom d'utilisateur incorrect.{END}")
        return False


def supp_users(nom, mdp):
    users = load_users()
    user = users[users["nom"] == nom]
    

    if user.empty:
        print(f"{RED}Utilisateur non trouvé.{END}")
        return

    user = user.iloc[0]
    hashed_mdp, salt = user["mot_de_passe"], eval(user["sel"])
    if hash_mdp(mdp, salt)[0] != hashed_mdp:
        print(f"{RED}Mot de passe incorrect.{END}")
        return

    
    supp_produits_par_utilisateur(user["user_id"])
    print(f"{GREEN}Utilisateur et ses produits supprimés !{END}")
    save_users(users)
