# Analysis Code

This folder contains the Python scripts used to conduct the empirical analyses and generate the main figures presented in the Master's thesis.

## Temporal Analysis

* **`time_patent_distribution.py`**
  Analyses the annual distribution of Enterprise AI patents over the 2015–2025 period and generates the corresponding temporal distribution figure.

* **`time_startups_distribution.py`**
  Analyses the annual distribution of Enterprise AI startups over the 2015–2025 period and generates the corresponding temporal distribution figure.

## Geographical Analysis

* **`nuts2_patent_distribution.py`**
  Calculates and visualises the geographical distribution of Enterprise AI patents across Dutch NUTS 2 regions.

* **`nuts2_startup_distribution.py`**
  Calculates and visualises the geographical distribution of Enterprise AI startups across Dutch NUTS 2 regions.

* **`nuts3_patent_distribution.py`**
  Calculates and visualises the geographical distribution of Enterprise AI patents across NUTS 3 (COROP) regions.

* **`nuts3_startup_distribution.py`**
  Calculates and visualises the geographical distribution of Enterprise AI startups across NUTS 3 (COROP) regions.

* **`LQ_map.py`**
  Calculates Location Quotients (LQ) and generates maps comparing the relative regional concentration of patents and startups.

* **`nuts2_relative_orientation_activity.py`**
  Generates the combined regional overview comparing the relative orientation of patent and startup activity.

## Technological Analysis

* **`patent_cpc_analysis.py`**
  Classifies patents into technological categories based on Cooperative Patent Classification (CPC) codes and analyses their technological composition.

* **`startup_cpc_analysis.py`**
  Applies the corresponding CPC-based technological framework to the startup dataset and analyses the technological composition of Enterprise AI startups.

* **`regional_technological_profiles.py`**
  Compares the technological profiles of patents and startups across Dutch regions.

## Notes

The scripts were developed for the empirical analysis of the Master's thesis and correspond to the methodological procedures and results reported in the thesis.

Input datasets are not included in this repository. File paths may therefore need to be adjusted before running the scripts.

