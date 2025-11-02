
# This code analyzes financial performance and generates charts for the top 10 and bottom 10 companies in the portfolio

import pandas as pd
import matplotlib.pyplot as plt

# Fichiers sur le Desktop
composition_path = r"C:/Users/.../Datathon_2025/Compagnies_sp500.csv"
stocks_path = r"C:/Users/.../Datathon_2025/Stocks_performance.csv"

# Charger les fichiers
sp500 = pd.read_csv(composition_path)
stocks = pd.read_csv(stocks_path)

# Fusionner par symbole
data = pd.merge(sp500, stocks, on="Symbol", how="left")

# ----------------------------
# 1️⃣ Top 10 entreprises par poids
top_weight = data.sort_values("Weight", ascending=False).head(10)
plt.bar(top_weight["Company"], top_weight["Weight"])
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 entreprises par poids dans le S&P 500")
plt.ylabel("Weight (%)")
plt.tight_layout()
plt.show()

# ----------------------------
# 2️⃣ Top 10 entreprises par bénéfice net
top_profit = data.sort_values("Net Income", ascending=False).head(10)
plt.bar(top_profit["Company"], top_profit["Net Income"])
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 entreprises par Net Income")
plt.ylabel("Net Income")
plt.tight_layout()
plt.show()

# ----------------------------
# 3️⃣ Top 10 entreprises en perte (Net Income négatif)
top_loss = data[data["Net Income"] < 0].sort_values("Net Income").head(10)
plt.bar(top_loss["Company"], top_loss["Net Income"])
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 entreprises en perte (Net Income négatif)")
plt.ylabel("Net Income")
plt.tight_layout()
plt.show()

# ----------------------------
# 4️⃣ Score de risque simple = Poids × perte (si perte)
data["Risk_Score"] = data.apply(lambda x: -x["Weight"] * x["Net Income"] if x["Net Income"] < 0 else 0, axis=1)
top_risk = data.sort_values("Risk_Score", ascending=False).head(10)

plt.bar(top_risk["Company"], top_risk["Risk_Score"])
plt.xticks(rotation=45, ha="right")
plt.title("Top 10 entreprises à risque (Poids × Perte)")
plt.ylabel("Risk Score")
plt.tight_layout()
plt.show()
