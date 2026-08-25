import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# ============================================================
# 1. FILE PATHS
# ============================================================

PATENT_FILE = "/Users/constancapaixao/Desktop/TESE/data/lens_with_nuts3.xlsx"
STARTUP_FILE = "/Users/constancapaixao/Desktop/TESE/data/startups-combined-updated.xlsx"

PATENT_SHEET = 0
STARTUP_SHEET = "Combined Startups"



# ============================================================
# 2. LOAD PATENT DATA
# ============================================================

# Main patent information
patents_main = pd.read_excel(
    PATENT_FILE,
    sheet_name="Enterprise AI Patents"
)

# NUTS 3 classification
patents_nuts3 = pd.read_excel(
    PATENT_FILE,
    sheet_name="NUTS 3 (per patent)"
)

print("PATENT MAIN COLUMNS:")
print(patents_main.columns.tolist())

print("\nPATENT NUTS3 COLUMNS:")
print(patents_nuts3.columns.tolist())


# ============================================================
# 3. MERGE PATENT CPC + NUTS 3 DATA
# ============================================================

patents = patents_main.merge(
    patents_nuts3[
        [
            "Patent ID",
            "NUTS 3 Sub-region",
            "NUTS 3 Code",
            "NUTS 2 Code"
        ]
    ],
    on="Patent ID",
    how="left"
)

print("\nPATENT COLUMNS AFTER MERGE:")
print(patents.columns.tolist())

print("\nNumber of patents:", len(patents))

print(
    "Patents with NUTS 3:",
    patents["NUTS 3 Sub-region"].notna().sum()
)


# ============================================================
# 4. LOAD STARTUP DATA
# ============================================================

startups = pd.read_excel(
    STARTUP_FILE,
    sheet_name="Combined Startups"
)

print("\nSTARTUP COLUMNS:")
print(startups.columns.tolist())


# ============================================================
# 5. CLEAN STARTUP DATA
# ============================================================

# Remove blank rows
startups = startups[
    startups["Name / Applicant"].notna()
].copy()

# Remove legend row
startups = startups[
    startups["Name / Applicant"]
    .astype(str)
    .str.strip()
    .str.lower()
    != "legend:"
].copy()

print("\nNumber of startups:", len(startups))


# ============================================================
# 6. COLUMN NAMES
# ============================================================

PATENT_NUTS3_COL = "NUTS 3 Sub-region"
PATENT_CPC_COL = "CPC Codes"

STARTUP_NUTS3_COL = "NUTS 3 Sub-region"
STARTUP_CPC_COL = "CPC Codes"


# ============================================================
# 7. TECHNOLOGICAL CATEGORIES
# ============================================================

CATEGORIES = {

    "Neural Networks /\nDeep Learning": [
        "G06N3"
    ],

    "Machine\nLearning": [
        "G06N20"
    ],

    "Computer\nVision": [
        "G06V10"
    ],

    "Vision\nApplications": [
        "G06V20"
    ],

    "Image\nAnalysis": [
        "G06T7"
    ],

    "Business\nProcess AI": [
        "G06Q10"
    ],

    "Sector-Specific\nAI": [
        "G06Q50"
    ]
}


# ============================================================
# 8. REGIONS INCLUDED IN THE HEATMAP
# ============================================================

REGIONS = [
    "Zuidoost-Noord-Brabant",
    "Groot-Amsterdam",
    "Utrecht",
    "Groot-Rijnmond",
    "Delft en Westland"
]


# ============================================================
# 9. CLEAN CPC CODES
# ============================================================

def clean_cpc_codes(value):

    if pd.isna(value):
        return []

    value = str(value).upper()

    # Split CPC codes using common separators
    codes = re.split(r"[;,\n|]+", value)

    cleaned_codes = []

    for code in codes:

        code = code.strip()

        # Remove spaces
        code = code.replace(" ", "")

        if code:
            cleaned_codes.append(code)

    return cleaned_codes


# ============================================================
# 10. CLASSIFY CPC CODES INTO TECHNOLOGICAL CATEGORIES
# ============================================================

def classify_categories(cpc_value):

    codes = clean_cpc_codes(cpc_value)

    categories_found = set()

    for code in codes:

        for category, prefixes in CATEGORIES.items():

            for prefix in prefixes:

                if code.startswith(prefix):

                    categories_found.add(category)

    return categories_found


# ============================================================
# 11. CREATE REGIONAL TECHNOLOGICAL MATRIX
# ============================================================

def create_matrix(df, region_col, cpc_col):

    df = df.copy()

    # Clean region names
    df[region_col] = (
        df[region_col]
        .astype(str)
        .str.strip()
    )

    # Assign technological categories
    df["TECH_CATEGORIES"] = (
        df[cpc_col]
        .apply(classify_categories)
    )

    # Empty result matrix
    matrix = pd.DataFrame(
        index=REGIONS,
        columns=list(CATEGORIES.keys()),
        dtype=float
    )

    regional_counts = {}

    for region in REGIONS:

        # Select observations in region
        region_df = df[
            df[region_col] == region
        ].copy()

        n_region = len(region_df)

        regional_counts[region] = n_region

        for category in CATEGORIES.keys():

            if n_region == 0:

                percentage = 0

            else:

                count = region_df[
                    region_df["TECH_CATEGORIES"].apply(
                        lambda categories:
                        category in categories
                    )
                ].shape[0]

                percentage = (
                    count / n_region
                ) * 100

            matrix.loc[
                region,
                category
            ] = percentage

    return matrix, regional_counts


# ============================================================
# 12. BUILD PATENT MATRIX
# ============================================================

patent_matrix, patent_counts = create_matrix(
    patents,
    PATENT_NUTS3_COL,
    PATENT_CPC_COL
)


# ============================================================
# 13. BUILD STARTUP MATRIX
# ============================================================

startup_matrix, startup_counts = create_matrix(
    startups,
    STARTUP_NUTS3_COL,
    STARTUP_CPC_COL
)


# ============================================================
# 14. PRINT RESULTS FOR CONTROL
# ============================================================

print("\n===================================")
print("PATENT REGIONAL COUNTS")
print("===================================")

for region, n in patent_counts.items():

    print(
        f"{region}: {n}"
    )


print("\nPATENT TECHNOLOGICAL MATRIX (%)")

print(
    patent_matrix.round(1)
)


print("\n===================================")
print("STARTUP REGIONAL COUNTS")
print("===================================")

for region, n in startup_counts.items():

    print(
        f"{region}: {n}"
    )


print("\nSTARTUP TECHNOLOGICAL MATRIX (%)")

print(
    startup_matrix.round(1)
)


# ============================================================
# 15. REGION LABELS INCLUDING SAMPLE SIZE
# ============================================================

patent_labels = [

    f"{region} (n={patent_counts[region]})"

    for region in REGIONS
]

startup_labels = [

    f"{region} (n={startup_counts[region]})"

    for region in REGIONS
]


# ============================================================
# 16. CREATE FIGURE
# ============================================================

fig, axes = plt.subplots(
    2,
    1,
    figsize=(13, 10)
)


# ============================================================
# 17. COMMON COLOUR SCALE
# ============================================================

VMIN = 0
VMAX = 75


# ============================================================
# 18. PATENT HEATMAP
# ============================================================

im1 = axes[0].imshow(
    patent_matrix.values.astype(float),
    cmap="Blues",
    vmin=VMIN,
    vmax=VMAX,
    aspect="auto"
)

axes[0].set_title(
    "A. Patents",
    fontsize=13,
    fontweight="bold",
    pad=12
)


# X-axis categories
axes[0].set_xticks(
    np.arange(
        len(CATEGORIES)
    )
)

axes[0].set_xticklabels(
    list(CATEGORIES.keys()),
    fontsize=10
)


# Y-axis regions
axes[0].set_yticks(
    np.arange(
        len(REGIONS)
    )
)

axes[0].set_yticklabels(
    patent_labels,
    fontsize=10
)


# ============================================================
# 19. ADD PATENT PERCENTAGES TO CELLS
# ============================================================

for i in range(
    len(REGIONS)
):

    for j in range(
        len(CATEGORIES)
    ):

        value = patent_matrix.iloc[
            i,
            j
        ]

        # Use white text on darker cells
        if value >= 40:

            text_color = "white"

        else:

            text_color = "black"

        # Show dash instead of 0.0%
        if value == 0:

            label = "–"

        else:

            label = f"{value:.1f}%"

        axes[0].text(
            j,
            i,
            label,
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
            color=text_color
        )


# ============================================================
# 20. STARTUP HEATMAP
# ============================================================

im2 = axes[1].imshow(
    startup_matrix.values.astype(float),
    cmap="Purples",
    vmin=VMIN,
    vmax=VMAX,
    aspect="auto"
)

axes[1].set_title(
    "B.Startups",
    fontsize=13,
    fontweight="bold",
    pad=12
)


# X-axis categories
axes[1].set_xticks(
    np.arange(
        len(CATEGORIES)
    )
)

axes[1].set_xticklabels(
    list(CATEGORIES.keys()),
    fontsize=10
)


# Y-axis regions
axes[1].set_yticks(
    np.arange(
        len(REGIONS)
    )
)

axes[1].set_yticklabels(
    startup_labels,
    fontsize=10
)


# ============================================================
# 21. ADD STARTUP PERCENTAGES TO CELLS
# ============================================================

for i in range(
    len(REGIONS)
):

    for j in range(
        len(CATEGORIES)
    ):

        value = startup_matrix.iloc[
            i,
            j
        ]

        if value >= 40:

            text_color = "white"

        else:

            text_color = "black"

        if value == 0:

            label = "–"

        else:

            label = f"{value:.1f}%"

        axes[1].text(
            j,
            i,
            label,
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
            color=text_color
        )


# ============================================================
# 22. GRID BETWEEN CELLS
# ============================================================

for ax in axes:

    ax.set_xticks(
        np.arange(
            -0.5,
            len(CATEGORIES),
            1
        ),
        minor=True
    )

    ax.set_yticks(
        np.arange(
            -0.5,
            len(REGIONS),
            1
        ),
        minor=True
    )

    ax.grid(
        which="minor",
        color="white",
        linestyle="-",
        linewidth=2
    )

    ax.tick_params(
        which="minor",
        bottom=False,
        left=False
    )

    ax.tick_params(
        axis="x",
        length=0
    )

    ax.tick_params(
        axis="y",
        length=0
    )


# ============================================================
# 23. MAIN FIGURE TITLE
# ============================================================

fig.suptitle(
    "Technological Profiles of the Main Dutch Enterprise AI Regions\n"
    "Netherlands · 2015–2025",
    fontsize=16,
    fontweight="bold",
    y=0.98
)


# ============================================================
# 24. COLOUR BARS
# ============================================================

cbar1 = fig.colorbar(
    im1,
    ax=axes[0],
    fraction=0.025,
    pad=0.02
)

cbar1.set_label(
    "% of patents in region",
    fontsize=10
)


cbar2 = fig.colorbar(
    im2,
    ax=axes[1],
    fraction=0.025,
    pad=0.02
)

cbar2.set_label(
    "% of startups in region",
    fontsize=10
)


# ============================================================
# 25. FINAL LAYOUT
# ============================================================

plt.subplots_adjust(
    left=0.22,
    right=0.92,
    top=0.89,
    bottom=0.08,
    hspace=0.28
)

# ============================================================
# 26. SAVE FIGURE
# ============================================================

plt.savefig(
    "../regional_technological_profiles.png",
    dpi=300,
    bbox_inches="tight"
)


# ============================================================
# 27. SHOW FIGURE
# ============================================================

plt.show()