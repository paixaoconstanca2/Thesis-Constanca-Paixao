import pandas as pd
import matplotlib.pyplot as plt

# Load Excel
file_path = "/Users/constancapaixao/Desktop/TESE/data/lens export 3 - clean.xlsx"
df = pd.read_excel(file_path, sheet_name="Enterprise AI Patents")

# Ensure Year is numeric
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

# Count patents per year
years = list(range(2015, 2026))

year_counts = (
    df[df["Year"].between(2015, 2025)]["Year"]
    .value_counts()
    .reindex(years, fill_value=0)
    .sort_index()
)

# Plot
plt.figure(figsize=(12, 6))

# Bars
plt.bar(
    year_counts.index,
    year_counts.values,
    color="#2f6fa7"
)

# Value labels
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
# Title
plt.title(
    "Enterprise AI Patent Distribution by Year\nNetherlands · 2015–2025",
    fontsize=16,
    fontweight="bold"
)

# Axis labels
plt.xlabel("Publication Year", fontsize=12)
plt.ylabel("Number of Patents", fontsize=12)

plt.xticks(years, fontsize=11)
plt.yticks(fontsize=11)

# Add space above the highest bar
plt.ylim(0, max(year_counts.values) + 5)

# Grid
plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

# Keep grid behind bars
plt.gca().set_axisbelow(True)

plt.tight_layout()

# Save high-resolution figure
plt.savefig(
    "../patents_distribution_2015_2025.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()