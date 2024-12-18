from Modules.gestion_produits import aff_produits
from Modules.gestion_utilisateur import *
from Modules.gestion_csv_produits import *
import time

GREEN = "\033[1;32m"
RED = "\033[31m"
BLUE = "\033[94m"
JAUNE = "\033[33m"
END = "\033[0m" 
art = '''
╔═╗╦═╗╔═╗ ╦╔═╗╔╦╗  ╔═╗╦  ╔═╗╔═╗╦═╗╦╔╦╗╦ ╦╔╦╗╦╔═╗
╠═╝╠╦╝║ ║ ║║╣  ║   ╠═╣║  ║ ╦║ ║╠╦╝║ ║ ╠═╣║║║║║╣ 
╩  ╩╚═╚═╝╚╝╚═╝ ╩   ╩ ╩╩═╝╚═╝╚═╝╩╚═╩ ╩ ╩ ╩╩ ╩╩╚═╝'''

def formulaire():
    while True:
        print("\n=== FORMULAIRE ===")
        print("1. Connexion")
        print("2. Inscription")
        print("3. Quitter")
        choix = input(f"{BLUE}Choisissez une option : {END}")

        if choix == "1":
            nom = input(f"{GREEN}Nom : {END}")
            mdp = input(f"{GREEN}Mot de passe : {END}")
            user_id = login_user(nom, mdp)
            if user_id:
                session_utilisateur(user_id)

        elif choix == "2":
            nom = input(f"{GREEN}Nom : {END}")
            mdp = input(f"{GREEN}Mot de passe : {END}")
            add_users(nom, mdp)

        elif choix == "3":
            print(f"{RED}Au revoir !{END}")
            break
        else:
            print(f"{RED}Choix invalide !{END}")


def session_utilisateur(user_id):
    while True:
        print("\n=== SESSION UTILISATEUR ===")
        print("1. Gérer mes produits")
        print("2. Supprimer mon compte")
        print("3. Déconnexion")
        choix = input(f"{BLUE}Choisissez une option : {END}")

        if choix == "1":
            menu_principal(user_id)

        elif choix == "2":
            nom = input(f"{GREEN}Confirmez votre nom : {END}")
            mdp = input(f"{GREEN}Confirmez votre mot de passe : {END}")
            supp_users(nom, mdp)
            break

        elif choix == "3":
            print(f"{RED}Déconnexion...{END}")
            break
        else:
            print(f"{RED}Choix invalide !{END}")


def menu_principal(nom_utilisateur):
    while True:
        print("\n=== GESTION DES PRODUITS ===")
        print("1. Ajouter un produit")
        print("2. Afficher mes produits")
        print("3. Supprimer un produit")
        print("4. Retour")
        choix = input(f"{BLUE}Choisissez une option : {END}")

        if choix == "1":
            nom = input(f"{GREEN}Nom du produit : {END}")
            prix = float(input(f"{GREEN}Prix : {END}"))
            quantite = int(input(f"{GREEN}Quantité : {END}"))
            add_produit(nom, prix, quantite, nom_utilisateur)

        elif choix == "2":  # Afficher les produits
            produits = load_produits()
            mes_produits = produits[produits["nom_utilisateur"] == nom_utilisateur]
            if not mes_produits.empty:
                aff_produits(mes_produits)
            else:
                print(f"{RED}Vous n'avez aucun produit.{END}")

        elif choix == "3":  # Supprimer un produit
            produits = load_produits()
            mes_produits = produits[produits["nom_utilisateur"] == nom_utilisateur]
            if not mes_produits.empty:
                nom = input(f"{GREEN}Nom du produit à supprimer : {END}")
                if nom in mes_produits["nom"].values:
                    supp_produit(nom, nom_utilisateur)
                    print(f"{GREEN}Produit supprimé avec succès !{END}")
                else:
                    print(f"{RED}Produit introuvable.{END}")
            else:
                print(f"{RED}Vous n'avez aucun produit à supprimer.{END}")

        elif choix == "4":
            break
        else:
            print(f"{RED}Choix invalide !{END}")



if __name__ == "__main__":
    create_userfile()
    create_produit()
    formulaire()