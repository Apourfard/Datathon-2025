
# This code analyzes financial performance and automatically generates charts for the top 10 and bottom 10 companies in the portfolio


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Dossier où les fichiers sont situés
folder = r"C:/Users/.../Datathon_2025"

# Chemins des fichiers
composition_path = os.path.join(folder, "Compagnie_sp500.csv")
stocks_path = os.path.join(folder, "Stocks_performance.csv")

# Charger les fichiers
sp500 = pd.read_csv(composition_path)
stocks = pd.read_csv(stocks_path)

# Fusionner les deux fichiers par symbole
data = pd.merge(sp500, stocks, on="Symbol", how="left")

# Nettoyage des colonnes numériques
for col in ["Weight", "Net Income"]:
    data[col] = (
        data[col]
        .astype(str)
        .str.replace(r"[\$,]", "", regex=True)   # retire $, et ,
        .str.replace(r"%", "", regex=False)      # retire %
        .str.replace(r"\((.*)\)", r"-\1", regex=True)  # transforme (123) -> -123
    )
    data[col] = pd.to_numeric(data[col], errors="coerce")

# Remplacer NaN par 0
data["Weight"] = data["Weight"].fillna(0)
data["Net Income"] = data["Net Income"].fillna(0)

# Normaliser le poids pour que la somme soit exactement 1
data["Weight_normalized"] = data["Weight"] / data["Weight"].sum()

# Créer un dossier pour enregistrer les graphiques
output_folder = os.path.join(folder, "Graphiques")
os.makedirs(output_folder, exist_ok=True)

# 1. Top 10 entreprises par poids
top_weight = data.sort_values("Weight", ascending=False).head(10)
plt.figure(figsize=(12,6))
plt.bar(top_weight["Company"], top_weight["Weight"])
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 entreprises par poids dans le S&P 500")
plt.ylabel("Weight (%)")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "Top_10_Weight.png"))
plt.close()

# 2. Top 10 entreprises par Net Income (profit)
top_profit = data.sort_values("Net Income", ascending=False).head(10)
plt.figure(figsize=(12,6))
plt.bar(top_profit["Company"], top_profit["Net Income"])
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 entreprises par Net Income")
plt.ylabel("Net Income")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "Top_10_Profit.png"))
plt.close()

# 3. Top 10 entreprises en perte (Net Income négatif)
top_loss = data[data["Net Income"] < 0].sort_values("Net Income").head(10)
if not top_loss.empty:
    plt.figure(figsize=(12,6))
    plt.bar(top_loss["Company"], top_loss["Net Income"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 10 entreprises en perte (Net Income négatif)")
    plt.ylabel("Net Income")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "Top_10_Loss.png"))
    plt.close()

# 4. Top 10 entreprises à risque (Risk Score = Weight_normalized × Perte)
data["Risk_Score"] = np.where(data["Net Income"] < 0,
                              -data["Weight_normalized"] * data["Net Income"],
                              0)

nb_loss = (data["Net Income"] < 0).sum()
print("Nombre d'entreprises avec Net Income négatif :", nb_loss)
print(data[data["Net Income"] < 0][["Company", "Symbol", "Net Income", "Weight_normalized"]].head(10))

if nb_loss > 0:
    top_risk = data.sort_values("Risk_Score", ascending=False).head(10)
    plt.figure(figsize=(12,6))
    plt.bar(top_risk["Company"], top_risk["Risk_Score"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 10 entreprises à risque (Weight × Perte)")
    plt.ylabel("Risk Score")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "Top_10_Risk.png"))
else:
    print("Aucune entreprise en perte. Graphique de risque non généré.")

