# Digital Escapism & Socio-Economic Stress Analysis

**Student:** Ali Efe Okudan
**ID:** 34314
**University:** Sabancı University
**Course:** DSA210 – Introduction to Data Science, Spring 2026

> **Final submission (18 May 2026):** The consolidated final report,
> figures, and analysis-ready data snapshots live in
> [`Final/`](Final/). Start with
> [`Final/FINAL_REPORT.md`](Final/FINAL_REPORT.md). AI-usage disclosure
> for this stage: [`Final/AI_USAGE_FINAL.md`](Final/AI_USAGE_FINAL.md).

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
├── data_collection.py            # Downloads all raw data
├── data_processing.py            # Merges, cleans, and normalises data
├── 34314_AliEfeOkudan_EDA.ipynb  # Full EDA and hypothesis testing notebook
├── requirements.txt              # Python dependencies
├── merged_dataset.csv            # Final 36-month unified dataset
├── steamdb_chart_730.csv         # Raw CS2 SteamDB data
├── usdtry_2023_2025.csv          # Raw USD/TRY data
├── bist100_2023_2025.csv         # Raw BIST100 data
├── google_trends_TR.csv          # Raw Google Trends data (TR)
├── steam_cs2_clean.csv           # Cleaned Steam data (2023–2025 window)
├── fig_*.png                     # EDA and hypothesis test figures
├── ML/                           # All ML-stage deliverables
│   ├── 34314_AliEfeOkudan_ML.ipynb   # Advanced regression notebook
│   ├── 34314_AliEfeOkudan_ML.html    # HTML export of the above
│   ├── ml_features.csv               # Engineered feature matrix
│   ├── fig_ml_*.png                  # ML figures (CV split, residuals, importance, …)
│   ├── AI_USAGE.md                   # AI-assistance disclosure for ML stage
│   └── ML_Project/                   # Beginner-style intro-to-ML version
│       ├── ml_implementation.ipynb
│       ├── build_notebook.py
│       ├── REPORT.md
│       ├── results.csv
│       ├── predictions_vs_actual.png
│       └── feature_importance.png
│
└── Final/                        # Final submission (18 May milestone)
    ├── FINAL_REPORT.md               # Consolidated final report
    ├── AI_USAGE_FINAL.md             # AI disclosure for the final stage
    ├── figures/                      # Report-embedded copies of all figures
    └── data/                         # Snapshot of analysis-ready CSVs
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

**4. Run the EDA notebook**
```bash
jupyter notebook 34314_AliEfeOkudan_EDA.ipynb
```
Run all cells. The notebook produces all EDA visualisations and hypothesis test results.

**5. Run the ML notebook**
```bash
jupyter notebook ML/34314_AliEfeOkudan_ML.ipynb
```
Trains the regularised linear / tree models and reproduces all numbers in the holdout table below as well as the `fig_ml_*.png` figures.

---

## Key Findings

| Hypothesis | Test | Result |
|------------|------|--------|
| H1: USD/TRY → TR Gaming | Pearson r = 0.771, p < 0.001 | **Supported** |
| H2: Crisis vs Normal periods | Mann-Whitney U, p = 0.0009 | **Supported** |
| H3: Stress Index → TR Gaming | Pearson r = −0.052, p = 0.764 | Not supported |

H1 and H2 support the digital escapism hypothesis: as Turkey's currency depreciates and economic crisis conditions emerge, Steam gaming activity in Turkey increases significantly.

---

## ML Methods (`ML/34314_AliEfeOkudan_ML.ipynb`)

The second project milestone applies regression models to predict the Turkey-specific gaming proxy (`steam_trends_z`) from macro-economic features.

**Setup**
- Target: `steam_trends_z` (z-scored Google Trends `geo='TR'` for `cs2 / counter strike / steam`).
- Features (10 total): `usdtry_z`, `bist100_z`, `stress_index_z`, `steam_players_z`, `usdtry_lag1`, `usdtry_lag2`, `usdtry_roll3`, `time_index`, `crisis_period`, `usdtry × crisis` interaction.
- Train / test: 28-month training set + **6-month chronological holdout** (2025-07 → 2025-12).
- Cross-validation on training: 5-fold `TimeSeriesSplit` (walk-forward chronological validation). Scaling for the learned models is refit per fold inside `sklearn.Pipeline`.

**Models compared**
- Baselines: mean, naïve persistence (`ŷ_t = y_{t-1}`), univariate OLS on `usdtry_z`.
- Learned: Linear Regression, **Ridge**, **Lasso**, **ElasticNet** (all with `alpha` grid-searched), Random Forest, XGBoost (depth grid-searched).

**Holdout results (sorted by RMSE)**

| Model                | RMSE (z) | MAE (raw search-volume) | R²    |
|----------------------|---------:|------------------------:|------:|
| **ElasticNet**       | 0.568    | 2.05                    | 0.222 |
| Lasso                | 0.598    | 2.01                    | 0.137 |
| Ridge                | 0.608    | 2.07                    | 0.108 |
| OLS (usdtry only)    | 0.608    | 2.18                    | 0.107 |
| Persistence baseline | 0.711    | 2.71                    | −0.22 |
| XGBoost              | 0.736    | 2.49                    | −0.31 |
| Random Forest        | 0.754    | 2.62                    | −0.37 |
| Mean baseline        | 1.220    | 4.51                    | −2.59 |
| Linear (no reg.)     | 1.775    | 7.44                    | −6.61 |

**Takeaways**
- **ElasticNet gives the best score in this submitted run** and beats persistence by ~20% on RMSE.
- Regularised linear models > tree models > unregularised linear, exactly as expected for n ≈ 28 training rows with 10 features.
- Permutation importance on the holdout suggests `usdtry_z` and its lags carry the most predictive signal; `stress_index_z` is near zero, consistent with EDA H3 being unsupported.
- Generated figures (in `ML/`): `fig_ml_cv_split.png`, `fig_ml_model_comparison.png`, `fig_ml_pred_vs_actual.png`, `fig_ml_residuals.png`, `fig_ml_coefficients.png`, `fig_ml_importance.png`, `fig_ml_perm_importance.png`.

**Important limitation:** the `_z` columns and `crisis_period` flag were created during the earlier data-processing stage using the full 2023–2025 dataset. For this class milestone, I keep them for consistency with the EDA, but a stricter forecasting version should recompute normalisation statistics and the crisis threshold using only the training period.

A simpler intro-to-ML companion notebook (`ML/ML_Project/ml_implementation.ipynb`) is also included for transparency, alongside its short stand-alone report (`ML/ML_Project/REPORT.md`).

---

## AI Usage

AI assistance was used during this project as a coding-support tool. Disclosure for each stage:

- **EDA stage:** see the *AI Usage Log* section inside `34314_AliEfeOkudan_EDA.ipynb`.
- **ML stage:** see [`ML/AI_USAGE.md`](ML/AI_USAGE.md) for a detailed, task-by-task breakdown.
- **Final-report stage:** see [`Final/AI_USAGE_FINAL.md`](Final/AI_USAGE_FINAL.md) for the disclosure covering this submission.

All research questions, hypotheses, modelling decisions, and conclusions are the author's. AI suggestions were reviewed and verified before being kept.
