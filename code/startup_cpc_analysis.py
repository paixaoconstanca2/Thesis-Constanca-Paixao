import pandas as pd
import matplotlib.pyplot as plt
import re

from pathlib import Path


# 1. FILE PATHS AND LOAD DATA
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

EXCEL_FILE = DATA_DIR / "startups-combined-updated.xlsx"
OUTPUT_FILE = OUTPUT_DIR / "startup_technological_composition_final.png"

df = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Combined Startups"
)

print("Total rows:", len(df))
print("Unique startups:", df["Name / Applicant"].nunique())

# 2. TECHNOLOGICAL CATEGORIES
CATEGORIES = {

    "Business Process AI": ["G06Q10"],
    "Sector-Specific AI": ["G06Q50"],
    "Machine Learning": ["G06N20"],
    "Neural Networks / Deep Learning": ["G06N3"],
    "Image Analysis": ["G06T7"],
    "Computer Vision": ["G06V10"],
    "Vision Applications": ["G06V20"],
    "Human-Computer Interaction": ["G06F3"],
    "Healthcare Informatics": ["G16H"],
    "Radar / Sensors": ["G01S"],
    "Facial / Biometric Recognition": ["G06V40"],
    "Livestock / Agriculture": ["A01K29"],
    "Geophysical Sensing": ["G01V"]
}


# 3. CLEAN CPC CODES
def clean_cpc_codes(value):

    if pd.isna(value):
        return []

    value = str(value).upper()

    codes = re.split(r"[;,\n|]+", value)

    codes = [
        code.strip().replace(" ", "")
        for code in codes
        if code.strip()
    ]

    return codes


df["CPC_LIST"] = df["CPC Codes"].apply(clean_cpc_codes)


# 4. CLASSIFY EACH STARTUP
def classify_startup(cpc_list):

    categories_found = set()

    for code in cpc_list:

        for category, prefixes in CATEGORIES.items():

            if any(code.startswith(prefix) for prefix in prefixes):
                categories_found.add(category)

    return categories_found


df["TECH_CATEGORIES"] = df["CPC_LIST"].apply(classify_startup)


# 5. COUNT STARTUPS PER CATEGORY
category_counts = {
    category: 0
    for category in CATEGORIES
}

for categories in df["TECH_CATEGORIES"]:

    for category in categories:
        category_counts[category] += 1


results = pd.DataFrame(
    list(category_counts.items()),
    columns=["Technological Category", "Number of Startups"]
)

results = results[
    results["Number of Startups"] > 0
].copy()

results = results.sort_values(
    "Number of Startups",
    ascending=False
)

print("\nTECHNOLOGICAL COMPOSITION:")
print(results.to_string(index=False))

print(
    "\nTotal category assignments:",
    results["Number of Startups"].sum()
)


# 6. PREPARE GRAPH
plot_df = results.sort_values(
    "Number of Startups",
    ascending=True
)


# 7. CREATE FIGURE
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(
    plot_df["Technological Category"],
    plot_df["Number of Startups"],
    color="#8B6F8E",
    edgecolor="white",
    linewidth=0.6,
    height=0.65
)


# 8. ADD VALUES
max_val = plot_df["Number of Startups"].max()

for bar, value in zip(
    bars,
    plot_df["Number of Startups"]
):

    ax.text(
        bar.get_width() + max_val * 0.01,
        bar.get_y() + bar.get_height() / 2,
        str(int(value)),
        va="center",
        ha="left",
        fontsize=9,
        fontweight="bold",
        color="#333333"
    )


# 9. TITLE AND AXES
ax.set_title(
    "Enterprise AI Startups by Technological Category\n"
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
    "Technological Category",
    fontsize=11,
    labelpad=8
)


# 10. FORMAT
ax.tick_params(
    axis="both",
    labelsize=10
)

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.4,
    color="#AAAAAA"
)

ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_xlim(
    0,
    max_val * 1.15
)


# 11. SAVE

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
