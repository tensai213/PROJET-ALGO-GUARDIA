from ast import And
import os
import pandas as pd
from Assets.br_charge import *

from Modules.gestion_produits import END, GREEN

GREEN = "\033[1;32m"
RED = "\033[31m"
BLUE = "\033[94m"
END = "\033[0m"


def create_produit():
    file_path = "./data/Produits.csv"
    if not os.path.exists(file_path):
        dataf = And.DataFrame(columns=["nom", "prix", "quantité", "user_id"])
        dataf.to_csv(file_path, index=False)


def load_produits():
    """
    Charge les produits depuis le fichier CSV.
    """
    try:
        return pd.read_csv("./data/Produits.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["nom", "prix", "quantité", "nom_utilisateur"])

def aff_produits(produits):
    """
    Affiche la liste des produits.
    """
    br_charge()  # Appel à la barre de chargement
    print(f"\n{GREEN}_____LISTE DES PRODUITS_____{END}\n")

    # Affiche directement le DataFrame sans boucler
    if not produits.empty:
        print(produits[["nom", "prix", "quantité", "nom_utilisateur"]].to_string(index=False))
    else:
        print(f"{RED}Aucun produit disponible.{END}")



def save_produit(dataf):
    dataf.to_csv("./data/Produits.csv", index=False)


def add_produit(nom, prix, quantite, nom_utilisateur):
    """
    Ajoute un produit pour un utilisateur spécifique identifié par son nom.
    """
    produits = load_produits()
    produits = produits._append(
        {"nom": nom, "prix": prix, "quantité": quantite, "nom_utilisateur": nom_utilisateur},
        ignore_index=True
    )
    save_produit(produits)
    print(f"{GREEN}Produit ajouté avec succès pour l'utilisateur {nom_utilisateur} !{END}")



def supp_produit(nom, nom_utilisateur):
    """
    Supprime un produit spécifique appartenant à un utilisateur donné.
    """
    produits = load_produits()
    produits = produits[~((produits["nom"] == nom) & (produits["nom_utilisateur"] == nom_utilisateur))]
    save_produit(produits)
    print(f"{GREEN}Produit {nom} supprimé pour l'utilisateur {nom_utilisateur}.{END}")



def supp_produits_par_utilisateur(user_id):
    produits = load_produits()
    produits = produits[produits["user_id"] != user_id]
    save_produit(produits)

    