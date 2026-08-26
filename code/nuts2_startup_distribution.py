import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# 1. FILE PATHS AND LOAD DATA

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

EXCEL_FILE = DATA_DIR / "startups-combined-updated.xlsx"
OUTPUT_FILE = OUTPUT_DIR / "nuts2_startup_distribution_final.png"

df = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Combined Startups"
)

# Check column names
print(df.columns.tolist())

# Column containing the NUTS 2 province
NUTS2_COL = "NUTS 2 Province"


# 2. COUNT STARTUPS BY NUTS 2

# Remove observations without NUTS 2 classification
df_valid = df[df[NUTS2_COL].notna()].copy()

# Remove extra spaces
df_valid[NUTS2_COL] = df_valid[NUTS2_COL].astype(str).str.strip()

# Count startups by province
df_counts = (
    df_valid[NUTS2_COL]
    .value_counts()
    .rename_axis("Province")
    .reset_index(name="Count")
)

# 3. SORT
df_counts = df_counts.sort_values(
    "Count",
    ascending=True
)

# 4. FIGURE

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(
    df_counts["Province"],
    df_counts["Count"],
    color="#8B6F8E",
    edgecolor="white",
    height=0.65
)

# 5. ADD VALUES

for bar, val in zip(bars, df_counts["Count"]):
    ax.text(
        bar.get_width() + 0.3,
        bar.get_y() + bar.get_height() / 2,
        str(val),
        va="center",
        fontsize=9,
        color="#333333",
        fontweight="bold"
    )

# 6. FORMATTING

ax.set_title(
    "Enterprise AI Startup Distribution by NUTS 2 (Province)\n"
    "Netherlands · 2015–2025",
    fontsize=14,
    fontweight="bold",
    color="#1A1A2E",
    pad=16
)

ax.set_xlabel(
    "Number of Startups",
    fontsize=11,
    labelpad=8
)

ax.set_ylabel(
    "Province",
    fontsize=11,
    labelpad=8
)

ax.tick_params(
    axis="both",
    labelsize=10
)

ax.set_xlim(
    0,
    df_counts["Count"].max() * 1.18
)

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.4,
    color="#AAAAAA"
)

ax.spines[["top", "right"]].set_visible(False)

# 7. SAVE

plt.tight_layout()

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

