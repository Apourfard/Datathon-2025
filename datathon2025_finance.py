
# This code analyzes financial performance for the top 10 and bottom 10 companies in the portfolio


import pandas as pd

# Chemins des fichiers sur Desktop
composition_path = r"C:/Users/.../Datathon_2025/Companies_sp500.csv"
stocks_path = r"C:/Users/.../Datathon_2025/Stocks_performance.csv"

# Charger les fichiers CSV
sp500 = pd.read_csv(composition_path)
stocks = pd.read_csv(stocks_path)

# Fusionner par symbole
data = pd.merge(sp500, stocks, left_on="Symbol", right_on="Symbol", how="left")

# 1️⃣ Top 10 entreprises par poids dans le S&P 500
print("=== Top 10 entreprises par poids ===")
top_weight = data.sort_values("Weight", ascending=False).head(10)
print(top_weight[["Company", "Symbol", "Weight", "Price"]])
print("\n")

# 2️⃣ Top 10 entreprises par Net Income (profit)
print("=== Top 10 entreprises par Net Income ===")
top_profit = data.sort_values("Net Income", ascending=False).head(10)
print(top_profit[["Company", "Symbol", "Net Income", "Market Cap"]])
print("\n")

# 3️⃣ Top 10 entreprises avec Net Income négatif (perte)
print("=== Top 10 entreprises en perte (Net Income négatif) ===")
top_loss = data[data["Net Income"] < 0].sort_values("Net Income").head(10)
print(top_loss[["Company", "Symbol", "Net Income", "Market Cap"]])
