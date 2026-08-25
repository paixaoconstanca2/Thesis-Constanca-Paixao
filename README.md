# Enterprise AI Innovation in the Netherlands

This repository contains the Python code used for the empirical analysis conducted as part of my Master's thesis on the geographical distribution and regional specialisation of Enterprise AI innovation in the Netherlands.

## Research Question

**How do the geographical distributions of Enterprise AI patents and startups compare across the Netherlands, and what do these patterns reveal about regional specialisation?**

## Analysis

The repository contains code for:

* Temporal analysis of patents and startups (2015–2025)
* Geographical analysis at NUTS 2 level
* Geographical analysis at NUTS 3 (COROP) level
* Location Quotient (LQ) analysis
* CPC-based technological classification
* Regional technological profiles
* Patent–startup regional orientation

## Data

The empirical analysis is based on two datasets covering the period 2015–2025:

* **167 validated Enterprise AI patents**
* **101 Enterprise AI startups**

Patent data were collected using Lens.org. The startup dataset was manually compiled and validated using multiple sources.

The underlying datasets are not included in this repository.

## Geographical Analysis

The geographical analysis is conducted at two territorial levels:

* **NUTS 2** — Dutch provinces
* **NUTS 3** — COROP regions

Regional classifications follow the NUTS framework used in the thesis. Geographical boundary data used for mapping were obtained from Eurostat.

Regional patent and startup distributions are analysed using absolute counts, relative shares, and Location Quotients (LQ) to identify differences in the relative orientation of regional Enterprise AI activity.

## Technological Analysis

Patents and startups are classified according to a common technological framework based on Cooperative Patent Classification (CPC) codes.

For patents, CPC classifications were processed and aggregated into technological categories, with each patent counted only once within each category.

For startups, CPC codes were manually assigned based on their technological activities and subsequently aggregated using the same classification framework. Each startup is counted only once within each technological category.

This common framework enables comparison between the technological composition of patenting activity and startup activity at both national and regional levels.

## Repository Structure

```text
Thesis-Constanca-Paixao/
├── README.md
├── requirements.txt
└── code/
    ├── README.md
    ├── LQ_map.py
    ├── nuts2_patent_distribution.py
    ├── nuts2_relative_orientation_activity.py
    ├── nuts2_startup_distribution.py
    ├── nuts3_patent_distribution.py
    ├── nuts3_startup_distribution.py
    ├── patent_cpc_analysis.py
    ├── regional_technological_profiles.py
    ├── startup_cpc_analysis.py
    ├── time_patent_distribution.py
    └── time_startups_distribution.py
```

A detailed description of the purpose of each script is provided in `code/README.md`.

## Requirements

The analyses were conducted in Python. The required packages are listed in `requirements.txt`.

The main dependencies include:

* pandas
* numpy
* matplotlib
* geopandas
* openpyxl
* pyogrio

The required packages can be installed using:

```bash
pip install -r requirements.txt
```

## Running the Code

The scripts can be run individually according to the analysis required.

The underlying datasets are not included in this repository. Therefore, input file paths may need to be adjusted before running the scripts.

Some geographical analyses also require the corresponding Eurostat NUTS boundary files.

## Reproducibility

This repository documents the computational procedures used to conduct the temporal, geographical, technological, and regional specialisation analyses presented in the Master's thesis.

The code is provided to increase transparency regarding the data processing, analytical procedures, and visualisations used in the empirical analysis.

## Author

**Constança Paixão**

Master's Thesis, August 2026

