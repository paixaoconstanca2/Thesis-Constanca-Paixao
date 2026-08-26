import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import re


# 1. FILES
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

EXCEL_FILE = DATA_DIR / "lens_export_clean.xlsx"

OUTPUT_TABLE = OUTPUT_DIR / "Patent_Technological_Composition.xlsx"
OUTPUT_FIGURE = OUTPUT_DIR / "technological_composition_patents_final.png"

CPC_COL = "CPC Codes"


# 2. TECHNOLOGICAL CATEGORY MAP
CATEGORY_MAP = [
    ("G06N3",  "Neural Networks / Deep Learning"),
    ("G06N20", "Machine Learning"),
    ("G06V10", "Computer Vision"),
    ("G06V20", "Vision Applications"),
    ("G06V40", "Facial / Biometric Recognition"),
    ("G06T7",  "Image Analysis"),
    ("G06Q10", "Business Process AI"),
    ("G06Q50", "Sector-Specific AI"),
    ("G16H",   "Healthcare Informatics"),
    ("G01S",   "Radar / Sensors"),
    ("A01K",   "Livestock / Agriculture"),
    ("G01V",   "Geophysical Sensing"),
    ("G06F3",  "Human-Computer Interaction"),
]

CATEGORY_MAP.sort(
    key=lambda x: -len(x[0])
)



# 3. CLASSIFICATION FUNCTION
def classify_cpc(code):

    if pd.isna(code):
        return None

    code = str(code).strip()

    for prefix, label in CATEGORY_MAP:

        if code.startswith(prefix):
            return label

    return None


# 4. READ DATASET
df = pd.read_excel(
    EXCEL_FILE,
    usecols=[CPC_COL]
)


# 5. CLASSIFY EACH PATENT
patent_categories = []

for index, row in df.iterrows():

    cpc_raw = row[CPC_COL]

    codes = [
        code.strip()
        for code in str(cpc_raw).split(";")
        if code.strip()
    ]

    cleaned_codes = []

    for code in codes:

        if re.match(r"^[A-Z]\d{2}[A-Z]\d{4}/", code):
            continue

        cleaned_codes.append(code)

    categories_this_patent = set()

    for code in cleaned_codes:

        category = classify_cpc(code)

        if category:
            categories_this_patent.add(category)

    patent_categories.append(
        categories_this_patent
    )


# 6. COUNT UNIQUE PATENTS PER CATEGORY
category_counter = Counter()

for categories in patent_categories:

    for category in categories:
        category_counter[category] += 1


# 7. PRINT RESULTS
print("\n==============================================")
print("NUMBER OF PATENTS PER TECHNOLOGICAL CATEGORY")
print("==============================================\n")

for category, count in category_counter.most_common():
    print(f"{category}: {count}")

print("\nTOTAL PATENTS IN DATASET:")
print(len(df))

matched_patents = sum(
    1
    for categories in patent_categories
    if len(categories) > 0
)

print("\nPATENTS WITH AT LEAST ONE MATCHED CATEGORY:")
print(matched_patents)


# 8. CREATE TABLE
topic_counts = pd.DataFrame(
    category_counter.most_common(),
    columns=[
        "Technological Category",
        "Number of Patents"
    ]
)

topic_counts.to_excel(
    OUTPUT_TABLE,
    index=False
)

# 9. PREPARE GRAPH
plot_data = topic_counts.sort_values(
    "Number of Patents",
    ascending=True
)


# 10.  FIGURE
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(
    plot_data["Technological Category"],
    plot_data["Number of Patents"],
    color="#2E6DA4",
    edgecolor="white",
    linewidth=0.6,
    height=0.65
)


# 11. ADD VALUES
max_val = plot_data["Number of Patents"].max()

for bar in bars:

    value = int(
        bar.get_width()
    )

    ax.text(
        bar.get_width() + max_val * 0.01,
        bar.get_y() + bar.get_height() / 2,
        str(value),
        va="center",
        ha="left",
        fontsize=9,
        fontweight="bold",
        color="#333333"
    )


# 12. TITLE AND AXES
ax.set_title(
    "Enterprise AI Patents by Technological Category\n"
    "Netherlands · 2015–2025",
    fontsize=14,
    fontweight="bold",
    color="#1A1A2E",
    pad=16
)

ax.set_xlabel(
    "Number of Patents",
    fontsize=11,
    labelpad=8
)

ax.set_ylabel(
    "Technological Category",
    fontsize=11,
    labelpad=8
)


# 13. FORMATTING
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


# 14. SAVE
plt.tight_layout()

plt.savefig(
    OUTPUT_FIGURE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
