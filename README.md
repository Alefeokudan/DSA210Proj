# Digital Escapism & Socio-Economic Stress Analysis

**Student:** Ali Efe Okudan
**ID:** 34314
**University:** Sabancı University
**Course:** DSA210 – Introduction to Data Science, Spring 2026

---

## Motivation

This project investigates the **digital escapism hypothesis**: do individuals in Turkey increase their engagement with digital gaming during periods of socio-economic stress? By analyzing the relationship between macroeconomic volatility (USD/TRY exchange rate, BIST100 index) and Steam gaming activity in Turkey, I aim to determine whether digital gaming serves as a coping mechanism during financial instability.

---

## Data Sources

| Source | Description | Collection Method |
|--------|-------------|-------------------|
| **SteamDB** | CS2 (app 730) daily concurrent players (global reference) | Manual CSV download from steamdb.info |
| **yfinance** | USD/TRY exchange rate and BIST100 index, 2023–2025 | `yfinance` Python library |
| **Google Trends** | Search volume in Turkey for Steam/CS2 keywords — used as **Turkey-specific gaming proxy** | `pytrends` Python library (`geo='TR'`) |
| **Google Trends** | Search volume in Turkey for economic-stress keywords (`ekonomik kriz`, `enflasyon`, `dolar kur`, `issizlik`) | `pytrends` Python library (`geo='TR'`) |

> **Note on gaming proxy:** Steam does not publish country-level player counts. Google Trends search volume for Steam/CS2 in Turkey (`geo='TR'`) is used as the primary proxy for Turkish gaming activity.

**Analysis window:** 2023-01-01 to 2025-12-31 (36 monthly observations after resampling)

---

## Hypotheses

- **H1:** Rising USD/TRY (currency depreciation) is positively correlated with Steam gaming activity in Turkey
- **H2:** Steam gaming activity is significantly higher during economic crisis periods (USD/TRY ≥ 75th percentile) than normal periods
- **H3:** The composite economic-stress search index correlates with Steam gaming activity in Turkey

---

## Repository Structure

```
DSA210Proj/
├── data_collection.py          # Downloads all raw data
├── data_processing.py          # Merges, cleans, and normalises data
├── 34314_AliEfeOkudan_EDA.ipynb  # Full EDA and hypothesis testing notebook
├── requirements.txt            # Python dependencies
├── merged_dataset.csv          # Final 36-month unified dataset
├── steamdb_chart_730.csv       # Raw CS2 SteamDB data
├── usdtry_2023_2025.csv        # Raw USD/TRY data
├── bist100_2023_2025.csv       # Raw BIST100 data
├── google_trends_TR.csv        # Raw Google Trends data (TR)
├── steam_cs2_clean.csv         # Cleaned Steam data (2023–2025 window)
└── fig_*.png                   # EDA and hypothesis test figures
```

---

## How to Reproduce

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Collect data**
```bash
python data_collection.py
```
This downloads USD/TRY, BIST100, Google Trends data and cleans the SteamDB CSV. Outputs: `usdtry_2023_2025.csv`, `bist100_2023_2025.csv`, `google_trends_TR.csv`, `steam_cs2_clean.csv`.

**3. Process and merge data**
```bash
python data_processing.py
```
Resamples all series to monthly frequency, fills missing values, adds z-score normalisation and crisis period flag. Output: `merged_dataset.csv`.

**4. Run the notebook**
```bash
jupyter notebook 34314_AliEfeOkudan_EDA.ipynb
```
Run all cells. The notebook produces all EDA visualisations and hypothesis test results.

---

## Key Findings

| Hypothesis | Test | Result |
|------------|------|--------|
| H1: USD/TRY → TR Gaming | Pearson r = 0.771, p < 0.001 | **Supported** |
| H2: Crisis vs Normal periods | Mann-Whitney U, p = 0.0009 | **Supported** |
| H3: Stress Index → TR Gaming | Pearson r = −0.052, p = 0.764 | Not supported |

H1 and H2 support the digital escapism hypothesis: as Turkey's currency depreciates and economic crisis conditions emerge, Steam gaming activity in Turkey increases significantly.

---

## AI Usage

AI assistance (Claude Sonnet 4.6) was used during this project. All prompts, outputs, and modifications are documented in the **AI Usage Log** section of `34314_AliEfeOkudan_EDA.ipynb`, as required by DSA210 academic integrity guidelines.
