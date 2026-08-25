import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import os

# ============================================================
# 1. FILES
# ============================================================

SHAPEFILE = "/Users/constancapaixao/Desktop/TESE/data/NUTS_RG_01M_2024_4326/NUTS_RG_01M_2024_4326.shp"

EXCEL_FILE = "/Users/constancapaixao/Desktop/TESE/data/Mapa regional.xlsx"

SHEET_NAME = "NUTs3"


# ============================================================
# 2. CHECK FILES
# ============================================================

print("Shapefile exists:", os.path.exists(SHAPEFILE))
print("Excel exists:", os.path.exists(EXCEL_FILE))


# ============================================================
# 3. LOAD NUTS 2024 GEOGRAPHICAL DATA
# ============================================================

nuts = gpd.read_file(SHAPEFILE)

nl_nuts3 = nuts[
    (nuts["CNTR_CODE"] == "NL") &
    (nuts["LEVL_CODE"] == 3)
].copy()


# ============================================================
# 4. LOAD PATENT DATA
# ============================================================

regional_data = pd.read_excel(
    EXCEL_FILE,
    sheet_name=SHEET_NAME
)

regional_data = regional_data.rename(
    columns={
        "NUTS 3 Code": "NUTS_ID"
    }
)

regional_data["Patents"] = pd.to_numeric(
    regional_data["Patents"],
    errors="coerce"
)


# ============================================================
# 5. MERGE GEOGRAPHY + DATA
# ============================================================

map_data = nl_nuts3.merge(
    regional_data[["NUTS_ID", "Patents"]],
    on="NUTS_ID",
    how="left"
)

# Regions not present in Excel = 0 patents
map_data["Patents"] = map_data["Patents"].fillna(0)


# ============================================================
# 6. CLASSIFY PATENT COUNTS
# ============================================================

def classify_patents(value):

    if value == 0:
        return "0"

    elif value <= 2:
        return "1–2"

    elif value <= 5:
        return "3–5"

    elif value <= 10:
        return "6–10"

    elif value <= 20:
        return "11–20"

    else:
        return ">20"


map_data["Patent_category"] = map_data["Patents"].apply(
    classify_patents
)


# ============================================================
# 7. COLORS
# ============================================================

colors = {
    "0": "#FFFFFF",
    "1–2": "#DCEAF5",
    "3–5": "#B8D4E8",
    "6–10": "#84B5D3",
    "11–20": "#4F90BC",
    ">20": "#2F6FA7"
}

# ============================================================
# 8. CHECK CLASSIFICATION
# ============================================================

print("\nPatent classification:")

print(
    map_data[
        [
            "NUTS_ID",
            "NAME_LATN",
            "Patents",
            "Patent_category"
        ]
    ]
    .sort_values("Patents", ascending=False)
    .to_string(index=False)
)


# ============================================================
# 9. CREATE MAP
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 10)
)


# ============================================================
# 10. PLOT EACH CLASS
# ============================================================

category_order = [
    "0",
    "1–2",
    "3–5",
    "6–10",
    "11–20",
    ">20"
]

for category in category_order:

    subset = map_data[
        map_data["Patent_category"] == category
    ]

    if subset.empty:
        continue

    subset.plot(
        ax=ax,
        color=colors[category],
        edgecolor="white",
        linewidth=0.7
    )


# ============================================================
# 11. DRAW REGIONAL BOUNDARIES
# ============================================================

map_data.boundary.plot(
    ax=ax,
    color="white",
    linewidth=0.6
)


# ============================================================
# 12. TITLES
# ============================================================

fig.suptitle(
    "Enterprise AI Patents by NUTS 3 Region",
    fontsize=16,
    fontweight="bold",
    y=0.96
)

ax.set_title(
    "Netherlands · 2015–2025",
    fontsize=12,
    pad=10
)


# ============================================================
# 13. REMOVE AXES
# ============================================================

ax.axis("off")


# ============================================================
# 14. LEGEND
# ============================================================

legend_elements = [
    Patch(
        facecolor=colors["0"],
        edgecolor="#B0B0B0",
        label="0"
    ),
    Patch(
        facecolor=colors["1–2"],
        edgecolor="white",
        label="1–2"
    ),
    Patch(
        facecolor=colors["3–5"],
        edgecolor="white",
        label="3–5"
    ),
    Patch(
        facecolor=colors["6–10"],
        edgecolor="white",
        label="6–10"
    ),
    Patch(
        facecolor=colors["11–20"],
        edgecolor="white",
        label="11–20"
    ),
    Patch(
        facecolor=colors[">20"],
        edgecolor="white",
        label=">20"
    )
]

ax.legend(
    handles=legend_elements,
    title="Number of Patents",
    loc="lower left",
    frameon=False,
    fontsize=9,
    title_fontsize=10
)


# ============================================================
# 15. LAYOUT
# ============================================================

plt.tight_layout(
    rect=[0, 0, 1, 0.93]
)


# ============================================================
# 16. SAVE MAP
# ============================================================

plt.savefig(
    "/Users/constancapaixao/Desktop/TESE/data/Patents_Count_NUTS3_classes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()