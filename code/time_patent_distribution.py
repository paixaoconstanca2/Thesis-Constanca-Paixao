import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


# 1. FILES
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

EXCEL_FILE = DATA_DIR / "lens_export_clean.xlsx"
OUTPUT_FILE = OUTPUT_DIR / "patents_distribution_2015_2025.png"


# 2. LOAD DATA
df = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Enterprise AI Patents"
)

# 3.ENSURE YEAR IS NUMERIC
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

#4. COUNT PATENTS PER YEAR
years = list(range(2015, 2026))

year_counts = (
    df[df["Year"].between(2015, 2025)]["Year"]
    .value_counts()
    .reindex(years, fill_value=0)
    .sort_index()
)

#5. PLOT
plt.figure(figsize=(12, 6))

#6. BARS
plt.bar(
    year_counts.index,
    year_counts.values,
    color="#2f6fa7"
)

#7. VALUE LABELS 
offset = max(year_counts.values) * 0.025

for x, y in zip(year_counts.index, year_counts.values):
    plt.text(
        x,
        y + offset,
        str(int(y)),
        ha="center",
        va="bottom",
        fontsize=13,
        fontweight="bold"
    )
    
#8. TITLE
plt.title(
    "Enterprise AI Patent Distribution by Year\nNetherlands · 2015–2025",
    fontsize=16,
    fontweight="bold"
)

#9. AXIS LABEL
plt.xlabel("Publication Year", fontsize=12)
plt.ylabel("Number of Patents", fontsize=12)

plt.xticks(years, fontsize=11)
plt.yticks(fontsize=11)

#10. ADD SPCE ABOVE HIGHEST BAR
plt.ylim(0, max(year_counts.values) + 5)

#11. GRID
plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

#12. GRIDE BEHIND BARS
plt.gca().set_axisbelow(True)

plt.tight_layout()

#13. FIGURE
plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
