import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import Patch
from pathlib import Path

# 1. FILES
# Repository root
BASE_DIR = Path(__file__).resolve().parent.parent

# Input data
DATA_DIR = BASE_DIR / "data"

SHAPEFILE = (
    DATA_DIR
    / "NUTS_RG_01M_2024_4326"
    / "NUTS_RG_01M_2024_4326.shp"
)

EXCEL_FILE = DATA_DIR / "Mapa regional.xlsx"

SHEET_NAME = "NUTs3"

# Output directory
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "LQ_NUTS3_continuous.png"

# 2. CHECK FILES
print("Shapefile exists:", SHAPEFILE.exists())
print("Excel exists:", EXCEL_FILE.exists())


# 3. LOAD NUTS 2024 GEOGRAPHICAL DATA

nuts = gpd.read_file(SHAPEFILE)

nl_nuts3 = nuts[
    (nuts["CNTR_CODE"] == "NL") &
    (nuts["LEVL_CODE"] == 3)
].copy()

# 4. LOAD REGIONAL DATA
lq = pd.read_excel(
    EXCEL_FILE,
    sheet_name=SHEET_NAME
)

lq = lq.rename(
    columns={
        "NUTS 3 Code": "NUTS_ID"
    }
)

lq["Patents"] = pd.to_numeric(
    lq["Patents"],
    errors="coerce"
)

lq["Startups"] = pd.to_numeric(
    lq["Startups"],
    errors="coerce"
)

lq["LQ"] = pd.to_numeric(
    lq["LQ"],
    errors="coerce"
)

# 5. CORRECT LQ = 0 CASES
# Patents exist but startups = 0
# -> LQ = 0 according to the methodology used

lq.loc[
    (lq["Patents"] > 0) &
    (lq["Startups"] == 0),
    "LQ"
] = 0

# 6. MERGE GEOGRAPHY + DATA
map_data = nl_nuts3.merge(
    lq,
    on="NUTS_ID",
    how="left"
)

map_data["Patents"] = map_data["Patents"].fillna(0)
map_data["Startups"] = map_data["Startups"].fillna(0)


# 7. IDENTIFY SPECIAL CASES
# No observations in either dataset
no_observations = map_data[
    (map_data["Patents"] == 0) &
    (map_data["Startups"] == 0)
].copy()

# Startups exist, but patents = 0
# -> LQ undefined
undefined = map_data[
    (map_data["Patents"] == 0) &
    (map_data["Startups"] > 0)
].copy()

# Regions with a valid LQ
valid_lq = map_data[
    ~(
        ((map_data["Patents"] == 0) & (map_data["Startups"] == 0)) |
        ((map_data["Patents"] == 0) & (map_data["Startups"] > 0))
    )
].copy()

# 8. CHECK VALUES
print("\nValid LQ values:")

print(
    valid_lq[
        [
            "NUTS_ID",
            "NAME_LATN",
            "Patents",
            "Startups",
            "LQ"
        ]
    ]
    .sort_values("LQ")
    .to_string(index=False)
)

print("\nMinimum LQ:", valid_lq["LQ"].min())
print("Maximum LQ:", valid_lq["LQ"].max())

# 9. CREATE DIVERGING COLOUR MAP

# Patent-oriented -> Balanced -> Startup-oriented

cmap = LinearSegmentedColormap.from_list(
    "lq_diverging",
    [
        "#203F4D",   # dark blue
        "#47758A",   # blue
        "#D8D8D4",   # balanced / neutral
        "#92799A",   # purple
        "#674E6E"    # dark purple
    ],
    N=256
)


# 10. NORMALISE AROUND LQ = 1
# vcenter = 1 because LQ = 1 indicates equal relative orientation

norm = TwoSlopeNorm(
    vmin=valid_lq["LQ"].min(),
    vcenter=1,
    vmax=valid_lq["LQ"].max()
)


# 11. CREATE MAP


fig, ax = plt.subplots(
    figsize=(8, 10)
)

# 12. PLOT VALID LQ REGIONS

valid_lq.plot(
    column="LQ",
    ax=ax,
    cmap=cmap,
    norm=norm,
    edgecolor="white",
    linewidth=0.7
)

# 13. PLOT UNDEFINED REGIONS

if not undefined.empty:

    undefined.plot(
        ax=ax,
        color="#EEEEEE",
        edgecolor="white",
        linewidth=0.7
    )


# 14. PLOT NO OBSERVATION REGIONS

if not no_observations.empty:

    no_observations.plot(
        ax=ax,
        color="#FFFFFF",
        edgecolor="#B0B0B0",
        linewidth=0.7
    )

# 15. DRAW REGIONAL BOUNDARIES

map_data.boundary.plot(
    ax=ax,
    color="white",
    linewidth=0.6
)



# 16. TITLES
fig.suptitle(
    "Relative Orientation of Enterprise AI Activity",
    fontsize=16,
    fontweight="bold",
    x=0.5,
    y=0.97,
    ha="center"
)

fig.text(
    0.5,
    0.925,
    "Location Quotient by NUTS 3 Region · Netherlands",
    ha="center",
    va="center",
    fontsize=12
)

# 17. REMOVE AXES

ax.axis("off")

# 18. CONTINUOUS COLOUR BAR
sm = plt.cm.ScalarMappable(
    cmap=cmap,
    norm=norm
)

sm.set_array([])

cbar = fig.colorbar(
    sm,
    ax=ax,
    orientation="vertical",
    fraction=0.032,
    pad=0.035,
    shrink=0.72
)

cbar.ax.axhline(
    1,
    color="black",
    linewidth=1.2
)


# Main colour-bar label
cbar.set_label(
    "Location Quotient (LQ)",
    fontsize=10,
    labelpad=12
)

cbar.ax.tick_params(
    labelsize=9
)

# 19. ADD SIMPLE ORIENTATION LABELS

# Label above the colour bar
cbar.ax.text(
    0.5,
    1.03,
    "Startup-oriented",
    transform=cbar.ax.transAxes,
    ha="center",
    va="bottom",
    fontsize=9,
    fontweight="bold"
)

# Label below the colour bar
cbar.ax.text(
    0.5,
    -0.045,
    "Patent-oriented",
    transform=cbar.ax.transAxes,
    ha="center",
    va="top",
    fontsize=9,
    fontweight="bold"
)



# 20. SPECIAL CASE LEGEND


special_legend = [
    Patch(
        facecolor="#EEEEEE",
        edgecolor="#B0B0B0",
        label="LQ undefined (no patents)"
    ),
    Patch(
        facecolor="#FFFFFF",
        edgecolor="#B0B0B0",
        label="No observations"
    )
]

ax.legend(
    handles=special_legend,
    loc="lower left",
    bbox_to_anchor=(0.02, -0.015),
    frameon=False,
    fontsize=9,
    handlelength=2.0
)



# 21. LAYOUT


plt.tight_layout(
    rect=[0, 0.02, 0.94, 0.93]
)

# 22. SAVE

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
