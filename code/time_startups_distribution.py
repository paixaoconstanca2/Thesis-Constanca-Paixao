import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


# 1. FILE PATHS AND LOAD DATA
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

EXCEL_FILE = DATA_DIR / "startups-combined-updated.xlsx"
OUTPUT_FILE = OUTPUT_DIR / "startup_time_distribution_final.png"

df = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Combined Startups"
)

# Check column names
print(df.columns.tolist())


# 2. DEFINE YEAR COLUMN
YEAR_COL = "Founded / Patent Year"

# Extrair um ano de 4 dígitos da célula
df["Founded Year Clean"] = (
    df[YEAR_COL]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

# Converter para número
df["Founded Year Clean"] = pd.to_numeric(
    df["Founded Year Clean"],
    errors="coerce"
)

# Mostrar valores que não conseguiram ser convertidos
invalid_years = df[df["Founded Year Clean"].isna()][
    ["Name / Applicant", YEAR_COL]
]

if not invalid_years.empty:
    print("\nRows without a valid founding year:")
    print(invalid_years)


# 3. KEEP ONLY 2015–2025
df_period = df[
    (df["Founded Year Clean"] >= 2015) &
    (df["Founded Year Clean"] <= 2025)
].copy()


# 4. COUNT STARTUPS BY YEAR
years = list(range(2015, 2026))

year_counts = (
    df_period["Founded Year Clean"]
    .value_counts()
    .reindex(years, fill_value=0)
    .sort_index()
)

print("\nStartup counts by year:")
print(year_counts)

print("\nTotal startups represented:", int(year_counts.sum()))


# 5. CREATE FIGURE
fig, ax = plt.subplots(figsize=(12, 6))

# Purple bars
bars = ax.bar(
    year_counts.index,
    year_counts.values,
    color="#8B6F8E",
    width=0.8,
    zorder=2
)


# 6. ADD VALUES ABOVE BARS
offset = max(year_counts.values) * 0.025

for year, value in zip(year_counts.index, year_counts.values):
    ax.text(
        year,
        value + offset,
        str(int(value)),
        ha="center",
        va="bottom",
        fontsize=13,
        fontweight="bold",
        color="#111111",
        zorder=3
    )


# 7. TITLE AND AXES
ax.set_title(
    "Enterprise AI Startup Distribution by Year\n"
    "Netherlands · 2015–2025",
    fontsize=16,
    fontweight="bold",
    color="#111111",
    pad=8
)

ax.set_xlabel(
    "Founded Year",
    fontsize=12
)

ax.set_ylabel(
    "Number of Startups",
    fontsize=12
)

ax.set_xticks(years)

ax.tick_params(
    axis="both",
    labelsize=11
)


# 8. GRID AND FRAME
ax.grid(
    axis="y",
    linestyle="--",
    linewidth=0.8,
    alpha=0.4,
    zorder=0
)

ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_visible(True)

# Give enough space above the highest bar
ax.set_ylim(
    0,
    max(year_counts.values) + 3
)


# 9. SAVE AND SHOW
plt.tight_layout()

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
