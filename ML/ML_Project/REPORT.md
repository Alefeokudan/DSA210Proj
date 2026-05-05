# DSA210 — Machine Learning Report

**Author:** Ali Efe Okudan (34314)
**Course:** DSA210 — Introduction to Data Science (Spring 2026)
**Project:** Digital Escapism & Socio-Economic Stress Analysis
**Date:** 2026-05-05

---

## 1. Goal

This is the ML stage of my project. Building on the EDA, I want to see whether
Turkish macroeconomic indicators can **predict** monthly gaming interest in
Turkey. The EDA showed strong *correlation* between USD/TRY and gaming
(Pearson r = 0.771). The ML stage asks the next question: can a model trained
on past months predict gaming interest on **future, unseen** months?

**Target (y):** `steam_trends_z` — z-scored Google-Trends gaming-search
interest in Turkey.
**Features (X):** four monthly variables already available in
`merged_dataset.csv`:

| Feature | Meaning |
|---|---|
| `usdtry_z` | z-scored USD/TRY exchange rate |
| `bist100_z` | z-scored Borsa Istanbul 100 index |
| `stress_index_z` | z-scored composite financial-stress index |
| `crisis_period` | 1 if USD/TRY ≥ 75th percentile that month, else 0 |

The dataset has **36 monthly observations** (2023-01 → 2025-12) and zero
missing values after the cleaning done in the data-processing stage.

---

## 2. Method

I followed the standard intro-to-DS recipe.

### 2.1 Train / test split

Time series — random shuffles are not allowed because they leak future
information. I held out the **last 6 months (2025-07 → 2025-12)** as the test
set and used the previous **30 months** for training.

### 2.2 Models

Three models, increasing in complexity:

1. **Linear Regression** — baseline, no hyper-parameters.
2. **Ridge Regression** (`alpha = 1.0`) — adds L2 regularisation, useful when
   there are few rows.
3. **Random Forest** (`n_estimators=200`, `max_depth=4`, `random_state=42`) —
   non-linear ensemble of decision trees.

Every model is fit with `model.fit(X_train, y_train)` and evaluated on the
same six test months.

### 2.3 Metrics

| Metric | Direction | Interpretation |
|---|---|---|
| RMSE | lower is better | error in z-units, penalises big misses |
| MAE  | lower is better | average absolute error in z-units |
| R²   | higher is better | 1 = perfect, 0 = as good as predicting the mean, < 0 = worse than the mean |

---

## 3. Results

### 3.1 Test-set performance (6-month holdout, 2025-07 → 2025-12)

| Model | RMSE | MAE | R² |
|---|---:|---:|---:|
| **Linear Regression** | **0.628** | **0.501** | **0.047** |
| Ridge (α = 1.0) | 0.666 | 0.522 | −0.071 |
| Random Forest | 0.849 | 0.667 | −0.740 |

(Sorted by RMSE — lower is better.)

Source: `results.csv`.

### 3.2 What each model learned

**Linear coefficients** (sign + magnitude of effect on `steam_trends_z`):

| Feature | Linear | Ridge |
|---|---:|---:|
| `usdtry_z` | **+1.309** | **+0.857** |
| `bist100_z` | −0.468 | −0.112 |
| `stress_index_z` | −0.078 | −0.062 |
| `crisis_period` | −0.186 | +0.152 |

**Random Forest feature importance:**

| Feature | Importance |
|---|---:|
| `usdtry_z` | **0.740** |
| `bist100_z` | 0.204 |
| `stress_index_z` | 0.049 |
| `crisis_period` | 0.008 |

All three models agree that **USD/TRY is by far the most informative feature**.

### 3.3 Figures

Saved into this folder during notebook execution:

- `predictions_vs_actual.png` — actual vs each model's prediction over the
  6 test months.
- `feature_importance.png` — Random Forest feature-importance bar chart.

---

## 4. Discussion

**Linear models beat Random Forest.** With only 30 training rows, the Random
Forest does not have enough data to beat a well-specified linear model. Its
holdout R² is −0.74, meaning it does worse than just predicting the training
mean. This is a textbook small-data result: simple models generalise better
when n is small.

**USD/TRY drives the prediction.** Across all three models, USD/TRY is the
dominant feature. The linear coefficient (+1.31) says that a one-standard-
deviation increase in the lira's weakening corresponds to roughly +1.3
standard deviations of extra gaming interest — large effect. This **supports
Hypothesis 1** from the EDA in a predictive setting, although the small sample
means the result should still be interpreted cautiously.

**Why is R² only 0.047 even for the best model?** R² close to zero means the
linear model is only slightly better than predicting the average over the test
months. Two reasons:

1. The test window covers a relatively *flat* period for both USD/TRY and
   gaming (compared to the 2023 spike). When the target itself doesn't move
   much, R² gets crushed even when RMSE is reasonable.
2. With only four current-month features, we are missing dynamics: lagged
   reactions, seasonality, news shocks. The discussion below points to these.

**`crisis_period` is almost ignored.** The Random Forest gives it 0.008
importance and Ridge shrinks its coefficient toward zero. That makes sense:
the flag is *derived* from `usdtry_z` (≥ 75th percentile), so once the model
already has the continuous USD/TRY value, the binary version is redundant.

---

## 5. Limitations

1. **Tiny dataset.** 36 monthly rows is at the very low end for ML.
   Random Forest in particular struggles.
2. **Single holdout.** A 6-month block is one realisation; a different test
   window could give different numbers. Time-series cross-validation would be
   more robust.
3. **Precomputed normalisation.** The z-score columns and crisis flag were
   created in the earlier processing stage using the full 2023-2025 dataset.
   This keeps the ML stage consistent with the EDA, but a stricter forecasting
   version should recompute these values from the training period only.
4. **Only contemporaneous features.** No lags, no rolling means, no calendar
   effects. The model can't learn that gaming reacts a month or two *after*
   a currency shock.
5. **`steam_trends` is a proxy for player count.** Steam does not publish
   country-level player counts, so we use TR Google-Trends interest in
   "steam" as the closest available signal.

---

## 6. Conclusion

A simple Linear Regression on four macroeconomic features predicts Turkish
gaming interest on a 6-month holdout with RMSE = 0.628 and a positive R²
(0.047), beating both a regularised Ridge and a Random Forest. The positive
USD/TRY coefficient is consistent with the EDA finding: **when the lira
weakens, gaming interest in Turkey tends to rise**. Because this is a small
class project with only 36 monthly rows, the result is best read as supportive
evidence rather than a final forecasting model.

---

## 7. Files in this folder

| File | What it is |
|---|---|
| `ml_implementation.ipynb` | Executed notebook (all cells, plots embedded) |
| `build_notebook.py` | Script that builds and runs the notebook |
| `results.csv` | Test-set metrics (RMSE / MAE / R²) for the three models |
| `predictions_vs_actual.png` | Time-plot of predictions vs actual on test set |
| `feature_importance.png` | Random Forest feature-importance chart |
| `REPORT.md` | This report |

---

## 8. AI usage

Used Claude (Anthropic) as a coding assistant to scaffold the notebook
structure (cell-by-cell template) and review code style.
All ML decisions (target, features, train/test split, model choice,
metric interpretation, conclusions) are my own based on what we covered in
DSA210 lectures and the project's EDA findings. No outputs were copied
without verification — every number in this report comes from running
`ml_implementation.ipynb` on `merged_dataset.csv`.
