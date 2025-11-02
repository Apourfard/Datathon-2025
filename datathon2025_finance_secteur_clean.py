
# Nettoyage et normalisation
# Ce code va :
# 1) Charger le fichier.
# 2) Supprimer les colonnes inutiles.
# 3) Corriger les noms de colonnes (espaces, caractères spéciaux).
# 4) Convertir Weight et Net Income en valeurs numériques.
# 5) Afficher la répartition par secteur.

import pandas as pd
import os

# Chemin vers le fichier original
file_path = r"C:/Users/.../Datathon_2025/SP500_with_Sector.csv"

# Charger le fichier
data = pd.read_csv(file_path)

# Afficher les colonnes initiales
print("Colonnes originales :")
print(list(data.columns))
print("\n")

# Renommer les colonnes (enlever espaces, points, caractères spéciaux)
data.columns = data.columns.str.strip().str.replace(" ", "_").str.replace(".", "", regex=False)

# Supprimer les colonnes inutiles
cols_to_drop = [col for col in data.columns if col in ["#", "Company_Name"]]
data = data.drop(columns=cols_to_drop, errors="ignore")

# Conversion des colonnes numériques
for col in ["Weight", "Net_Income"]:
    data[col] = (
        data[col]
        .astype(str)
        .str.replace(r"[\$,()%]", "", regex=True)
        .str.replace(r"\((.*)\)", r"-\1", regex=True)
    )
    data[col] = pd.to_numeric(data[col], errors="coerce")

# Remplir les valeurs manquantes
data["Weight"] = data["Weight"].fillna(0)
data["Net_Income"] = data["Net_Income"].fillna(0)
data["Sector"] = data["Sector"].fillna("Unknown")

# Vérification rapide
print("Vérification des colonnes nettoyées :")
print(data.dtypes)
print("\n")

# Somme du poids (doit être proche de 1 ou 100)
print(f"Somme des poids : {data['Weight'].sum():.4f}")

# Comptage des entreprises par secteur
print("\nRépartition des entreprises par secteur :")
print(data["Sector"].value_counts().to_string())

# Sauvegarder le fichier nettoyé
output_path = r"C:/Users/.../Datathon_2025/SP500_with_Sector_Clean.csv"
data.to_csv(output_path, index=False)
print(f"\nFichier nettoyé enregistré sous : {output_path}")
