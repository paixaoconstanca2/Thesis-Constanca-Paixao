import pandas as pd
import matplotlib.pyplot as plt

FICHEIRO = "/Users/constancapaixao/Desktop/TESE/data/lens export 3 - clean.xlsx"

df = pd.read_excel(FICHEIRO)

CITY_TO_PROVINCE = {
    "Amsterdam": "Noord-Holland", "Amstelveen": "Noord-Holland", "Haarlem": "Noord-Holland",
    "Hilversum": "Noord-Holland", "Zaandam": "Noord-Holland", "Alkmaar": "Noord-Holland",
    "Rotterdam": "Zuid-Holland", "Delft": "Zuid-Holland", "Den Haag": "Zuid-Holland",
    "The Hague": "Zuid-Holland", "Leiden": "Zuid-Holland", "Dordrecht": "Zuid-Holland",
    "Eindhoven": "Noord-Brabant", "Tilburg": "Noord-Brabant", "Breda": "Noord-Brabant",
    "Helmond": "Noord-Brabant", "Den Bosch": "Noord-Brabant",
    "Utrecht": "Utrecht",
    "Arnhem": "Gelderland", "Nijmegen": "Gelderland", "Wageningen": "Gelderland",
    "Enschede": "Overijssel", "Hengelo": "Overijssel", "Zwolle": "Overijssel",
    "Groningen": "Groningen", "Leeuwarden": "Friesland",
    "Maastricht": "Limburg", "Venlo": "Limburg",
    "Almere": "Flevoland",
}

SKIP = ["Individual inventor", "USA", "Germany", "Belgium", "Finland", "India"]

def parse_province(region_str):
    if not region_str or any(k in str(region_str) for k in SKIP):
        return None
    first = str(region_str).split(";;")[0]
    parts = [p.strip() for p in first.split(",")]
    city = parts[0]
    province = parts[1] if len(parts) > 1 else None
    if province in CITY_TO_PROVINCE.values():
        return province
    return CITY_TO_PROVINCE.get(city)

province_counts = {}
for region_str in df["Applicant Region(s)"].dropna():
    prov = parse_province(region_str)
    if prov:
        province_counts[prov] = province_counts.get(prov, 0) + 1

region_df = pd.Series(province_counts).sort_values(ascending=True)
colors = ["#2E6DA4"] * len(region_df)


fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(region_df.index, region_df.values, color=colors, edgecolor="white", height=0.65)

for bar, val in zip(bars, region_df.values):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
            str(val), va="center", fontsize=9, color="#333333", fontweight="bold")

ax.set_title("Enterprise AI Patents by NUTS 2 (Province) \nNetherlands · 2015–2025",
             fontsize=14, fontweight="bold", color="#1A1A2E", pad=16)
ax.set_xlabel("Number of Patents", fontsize=11, labelpad=8)
ax.set_ylabel("Province", fontsize=11, labelpad=8)
ax.set_xlim(0, region_df.max() * 1.18)
ax.grid(axis="x", linestyle="--", alpha=0.4, color="#AAAAAA")
ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
plt.savefig("../distribution_by_region.png", dpi=180, bbox_inches="tight")
plt.show()