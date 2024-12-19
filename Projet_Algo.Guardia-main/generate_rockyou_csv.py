import hashlib
import pandas as pd

def hash_password(password):
    """
    Hache un mot de passe avec SHA-256.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_rockyou_csv(input_file="rockyou-75.txt", output_file="rockyou-75.csv"):
    """
    Transforme un fichier texte contenant des mots de passe en clair en un fichier CSV
    avec deux colonnes : 'mot_de_passe' (clair) et 'mot_de_passe_hash' (haché).
    """
    try:
        # Charger les mots de passe depuis le fichier texte
        with open(input_file, "r", encoding="utf-8", errors="ignore") as file:
            passwords = [line.strip() for line in file.readlines()]
        
        # Créer un DataFrame avec les mots de passe en clair
        data = pd.DataFrame(passwords, columns=["mot_de_passe"])

        # Ajouter une colonne avec les mots de passe hashés
        data["mot_de_passe_hash"] = data["mot_de_passe"].apply(hash_password)

        # Sauvegarder le fichier CSV
        data.to_csv(output_file, index=False, encoding="utf-8")
        print(f"Fichier CSV généré avec succès : {output_file}")

    except FileNotFoundError:
        print(f"Erreur : Le fichier {input_file} est introuvable.")

# Générer le fichier CSV
generate_rockyou_csv()
