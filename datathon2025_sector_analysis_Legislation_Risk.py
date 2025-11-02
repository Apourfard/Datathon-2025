import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# === 1. Load CSV ===
file_path = r"C:/Users/.../Datathon_2025/SP500_with_Sector_Clean.csv"
if not os.path.exists(file_path):
    raise SystemExit(f"File not found: {file_path}")

data = pd.read_csv(file_path)

# === 2. Basic cleaning ===
data["Weight"] = pd.to_numeric(data["Weight"], errors="coerce").fillna(0)
data["Net_Income"] = pd.to_numeric(data["Net_Income"], errors="coerce").fillna(0)
data["Sector"] = data["Sector"].fillna("Unknown")

# === 3. Normalize weight ===
total_weight = data["Weight"].sum()
data["Weight_normalized"] = data["Weight"] / total_weight if total_weight != 0 else 0.0

# === 4. Risk score ===
data["Risk_Score"] = np.where(data["Net_Income"] < 0, -data["Weight_normalized"] * data["Net_Income"], 0)

# === 5. Sector-based legislation exposure (H.R.1 provisions) ===
sector_legislation_mapping = {
    "Energy": 1.0,
    "Utilities": 0.8,
    "Materials": 0.8,
    "Industrials": 0.6,
    "Technology": 0.6,
    "Consumer Discretionary": 0.4,
    "Consumer Staples": 0.4,
    "Financials": 0.2,
    "Health Care": 0.2,
    "Real Estate": 0.2,
    "Communication Services": 0.2,
    "Unknown": 0.0
}

data["Sector_Legislation_Risk"] = data["Sector"].map(sector_legislation_mapping).fillna(0)

# === 6. Company-level adjusted legislation impact ===
data["Legislation_Impact"] = data["Sector_Legislation_Risk"] * data["Weight_normalized"] * data["Net_Income"].abs()

# === 6b. Normalize company-level legislation risk (0-1) ===
max_impact = data["Legislation_Impact"].max()
data["Legislation_Risk_Score"] = data["Legislation_Impact"] / max_impact if max_impact > 0 else 0

# === 6c. Print affected sectors ===
affected_sectors = data.loc[data["Legislation_Impact"] > 0, "Sector"].unique()
print("Législation H.R.1 – exposition sectorielle moyenne :")
print(data.groupby("Sector")["Sector_Legislation_Risk"].mean().sort_values(ascending=False))
print("Secteurs potentiellement affectés :", affected_sectors)
print("Nombre d'entreprises exposées :", data["Legislation_Impact"].count())

# === 7. Aggregate by sector ===
agg = data.groupby("Sector").agg(
    company_count=("Symbol", "count"),
    total_weight=("Weight_normalized", "sum"),
    avg_net_income=("Net_Income", "mean"),
    total_net_income=("Net_Income", "sum"),
    total_risk=("Risk_Score", "sum"),
    legislation_exposure=("Sector_Legislation_Risk", "mean"),
    total_legislation_impact=("Legislation_Impact", "sum")
).reset_index()

# === 8. Folder for graphs ===
graph_folder = os.path.join(os.path.dirname(file_path), "Graphiques_Secteurs")
os.makedirs(graph_folder, exist_ok=True)

def save_plot(fig, name):
    safe_name = "".join(c if c.isalnum() or c in ["_"] else "_" for c in name)
    path = os.path.join(graph_folder, f"{safe_name}.png")
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure saved: {path}")

# === 9. Top 10 sectors charts ===
for col, title, palette, fname in [
    ("total_weight", "Top 10 secteurs par poids", "viridis", "Top10_Poids"),
    ("total_risk", "Top 10 secteurs par risque", "magma", "Top10_Risque"),
    ("total_net_income", "Top 10 secteurs par Net Income", "coolwarm", "Top10_NetIncome"),
    ("total_legislation_impact", "Top 10 secteurs par impact législatif H.R.1", "crest", "Top10_LegislationImpact")
]:
    top10 = agg.sort_values(col, ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=col, y="Sector", data=top10, palette=palette, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(col.replace("_", " ").capitalize())
    ax.set_ylabel("Secteur")
    save_plot(fig, fname)

# === 10. Legislative exposure graph (average sector-level) ===
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(
    x="legislation_exposure",
    y="Sector",
    data=agg.sort_values("legislation_exposure", ascending=False),
    palette="crest",
    ax=ax
)
ax.set_title("Impact législatif moyen par secteur (H.R.1)")
ax.set_xlabel("Niveau moyen d'impact (0 = faible, 1 = fort)")
ax.set_ylabel("Secteur")
save_plot(fig, "Legislation_Impact_By_Sector")

# === 11. Top 3 risky companies per sector ===
for sector, df_sector in data.groupby("Sector"):
    top3 = df_sector[df_sector["Risk_Score"] > 0].sort_values("Risk_Score", ascending=False).head(3)
    if not top3.empty:
        fig, ax = plt.subplots(figsize=(8,4))
        sns.barplot(x="Risk_Score", y="Company", data=top3, palette="Reds_r", ax=ax)
        ax.set_title(f"Top 3 entreprises les plus risquées - {sector}")
        ax.set_xlabel("Risk Score")
        ax.set_ylabel("Entreprise")
        save_plot(fig, f"Top3_Risque_{sector}")

# === 12. Top 3 companies by legislative risk score per sector ===
for sector, df_sector in data.groupby("Sector"):
    top3_leg = df_sector[df_sector["Legislation_Risk_Score"] > 0].sort_values(
        "Legislation_Risk_Score", ascending=False
    ).head(3)
    if not top3_leg.empty:
        fig, ax = plt.subplots(figsize=(8,4))
        sns.barplot(x="Legislation_Risk_Score", y="Company", data=top3_leg, palette="Blues_r", ax=ax)
        ax.set_title(f"Top 3 entreprises par impact législatif - {sector}")
        ax.set_xlabel("Legislation Risk Score (0-1)")
        ax.set_ylabel("Entreprise")
        save_plot(fig, f"Top3_Legislation_{sector}")

# === 13. Export final CSV with all metrics ===
output_csv = os.path.join(os.path.dirname(file_path), "SP500_with_Legislation_Impact.csv")
data.to_csv(output_csv, index=False)
print(f"\nFinal CSV with all metrics saved: {output_csv}")

print("\nAnalyse terminée avec succès.")
print(f"Les graphiques sont enregistrés dans le dossier : {graph_folder}")
