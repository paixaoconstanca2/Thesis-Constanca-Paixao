import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pathlib import Path


#1. FILE PATHS


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

SHAPEFILE = (
    DATA_DIR
    / "NUTS_RG_01M_2024_4326"
    / "NUTS_RG_01M_2024_4326.shp"
)

EXCEL_FILE = DATA_DIR / "Mapa regional.xlsx"

SHEET_NAME = "NUTs2"

OUTPUT_FILE = OUTPUT_DIR / "LQ_NUTS2_Enterprise_AI.png"

#2. CHECK FILES

print("Shapefile exists:", SHAPEFILE.exists())
print("Excel exists:", EXCEL_FILE.exists())

# 3.LOAD NUTS 2024 GEOGRAPHICAL DATA

nuts = gpd.read_file(SHAPEFILE)

# 4.FILTER NETHERLANDS + NUTS 2

nl_nuts2 = nuts[
    (nuts["CNTR_CODE"] == "NL") &
    (nuts["LEVL_CODE"] == 2)
].copy()


print("\nDutch NUTS 2 regions:")
print(
    nl_nuts2[
        ["NUTS_ID", "NAME_LATN"]
    ].sort_values("NUTS_ID")
)

#5. LOAD LQ DATA FROM EXCEL

lq = pd.read_excel(
    EXCEL_FILE,
    sheet_name=SHEET_NAME
)


#6. RENAME EXCEL COLUMN


lq = lq.rename(
    columns={
        "NUTS 2 Code": "NUTS_ID"
    }
)


#7. MAKE SURE LQ IS NUMERIC

lq["LQ"] = pd.to_numeric(
    lq["LQ"],
    errors="coerce"
)


print("\nLQ data:")
print(lq)

#8. MERGE GEOGRAPHY + LQ DATA

map_data = nl_nuts2.merge(
    lq,
    on="NUTS_ID",
    how="left"
)


print("\nMerged data:")
print(
    map_data[
        ["NUTS_ID", "NAME_LATN", "LQ"]
    ].sort_values("NUTS_ID")
)


#9. CLASSIFY LQ VALUES

def classify_lq(value):

    if pd.isna(value):
        return "Undefined"

    elif value < 0.75:
        return "Patent-oriented"

    elif value <= 1.25:
        return "Balanced"

    else:
        return "Startup-oriented"


map_data["LQ_category"] = (
    map_data["LQ"].apply(classify_lq)
)


print("\nLQ classification:")
print(
    map_data[
        ["NUTS_ID", "NAME_LATN", "LQ", "LQ_category"]
    ].sort_values("NUTS_ID")
)


#10. COLORS


colors = {
    "Patent-oriented": "#3B6478",
    "Balanced": "#D8D8D4",
    "Startup-oriented": "#8B6F8E",
    "Undefined": "#F2F2F2"
}



#11. CREATE MAP

fig, ax = plt.subplots(
    figsize=(7, 9)
)


for category, color in colors.items():

    subset = map_data[
        map_data["LQ_category"] == category
    ]

    subset.plot(
        ax=ax,
        color=color,
        edgecolor="white",
        linewidth=1
    )


#12. TITLE


fig.suptitle(
    "Relative Orientation of Enterprise AI Activity",
    fontsize=16,
    fontweight="bold",
    y=0.97
)

ax.set_title(
    "Location Quotient by NUTS 2 Region · Netherlands",
    fontsize=12,
    pad=10
)

# 13.REMOVE AXES

ax.axis("off")

# 14. LEGEND

legend_elements = [

    Patch(
        facecolor="#3B6478",
        edgecolor="white",
        label="Patent-oriented (LQ < 0.75)"
    ),

    Patch(
        facecolor="#D8D8D4",
        edgecolor="white",
        label="Balanced (LQ 0.75–1.25)"
    ),

    Patch(
        facecolor="#8B6F8E",
        edgecolor="white",
        label="Startup-oriented (LQ > 1.25)"
    ),

    Patch(
        facecolor="#F2F2F2",
        edgecolor="#B0B0B0",
        label="LQ undefined"
    )
]


ax.legend(
    handles=legend_elements,
    loc="lower left",
    frameon=False,
    fontsize=10
)



# 15. FINAL LAYOUT

plt.tight_layout(rect=[0, 0, 1, 0.93])



#16. SAVE FIGURE

OUTPUT_FILE = (
    "/Users/constancapaixao/Desktop/TESE/data/"
    "LQ_NUTS2_Enterprise_AI.png"
)

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)


print("\nMap saved to:")
print(OUTPUT_FILE)

# 17.SHOW FIGURE

plt.show()
