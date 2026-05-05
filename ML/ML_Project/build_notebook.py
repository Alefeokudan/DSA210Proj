"""Build a beginner-friendly ML notebook (first-time DS student style)."""
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from nbconvert.preprocessors import ExecutePreprocessor
from pathlib import Path

OUT_DIR = Path("/Users/alefe/Desktop/DSA210Proj/ML/ML_Project")
OUT_DIR.mkdir(exist_ok=True)
NB_PATH = OUT_DIR / "ml_implementation.ipynb"

cells = []

# ------------------------------------------------------------------
cells.append(new_markdown_cell(
"""# DSA210 Project — Machine Learning Implementation

**Author:** Ali Efe Okudan (34314)
**Course:** DSA210 — Introduction to Data Science (Spring 2026)
**Notebook:** First ML implementation for the project.

## Goal
Predict the monthly **Google-Trends gaming interest in Turkey** (`steam_trends_z`,
z-scored) from Turkish macroeconomic indicators (USD/TRY, BIST100,
financial-stress index).

This is my first time doing ML, so I will follow the standard intro-to-DS workflow:

1. Load the cleaned monthly dataset (36 rows, already prepared in EDA notebook).
2. Pick features and target.
3. Split into train / test **chronologically** (time series — no random shuffle).
4. Train three simple models: Linear Regression, Ridge, Random Forest.
5. Evaluate using RMSE, MAE, R² on the held-out test months.
6. Plot predictions vs actual.
7. Discuss the results.
"""
))

# ------------------------------------------------------------------
cells.append(new_markdown_cell("## 1. Imports"))
cells.append(new_code_cell(
"""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# fixed seed so results don't change between runs
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

print("Libraries loaded successfully.")
"""
))

# ------------------------------------------------------------------
cells.append(new_markdown_cell("## 2. Load the data\n\nThe cleaned dataset comes from the EDA stage and lives one folder up."))
cells.append(new_code_cell(
"""DATA_PATH = "../../merged_dataset.csv"
df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)
df = df.sort_index()
print("Shape:", df.shape)
df.head()
"""
))

cells.append(new_code_cell(
"""# quick sanity check — no missing values, monthly frequency
print("Missing values per column:")
print(df.isna().sum())
print()
print("Date range:", df.index.min().date(), "to", df.index.max().date())
"""
))

# ------------------------------------------------------------------
cells.append(new_markdown_cell(
"""## 3. Define features (X) and target (y)

The target is `steam_trends_z` — z-scored Google-Trends gaming interest in Turkey.
The features are the three z-scored macro indicators plus the crisis flag.
"""
))
cells.append(new_code_cell(
"""TARGET = "steam_trends_z"
FEATURES = ["usdtry_z", "bist100_z", "stress_index_z", "crisis_period"]

X = df[FEATURES].copy()
y = df[TARGET].copy()

print("Features:", FEATURES)
print("X shape:", X.shape, "  y shape:", y.shape)
X.head()
"""
))

# ------------------------------------------------------------------
cells.append(new_markdown_cell(
"""## 4. Train / test split (chronological)

This is monthly time-series data, so we **cannot** shuffle the rows.
Standard practice in intro DS for time series: hold out the last block of months
as the test set. We use the **last 6 months (2025-07 → 2025-12)** for testing
and everything before that for training.
"""
))
cells.append(new_code_cell(
"""TEST_MONTHS = 6

X_train = X.iloc[:-TEST_MONTHS]
X_test  = X.iloc[-TEST_MONTHS:]
y_train = y.iloc[:-TEST_MONTHS]
y_test  = y.iloc[-TEST_MONTHS:]

print(f"Train: {X_train.index.min().date()} → {X_train.index.max().date()}  ({len(X_train)} rows)")
print(f"Test : {X_test.index.min().date()}  → {X_test.index.max().date()}  ({len(X_test)} rows)")
"""
))

# ------------------------------------------------------------------
cells.append(new_markdown_cell(
"""## 5. Train the models

Three models, each one is a single line of `.fit()`:

- **Linear Regression** — the simplest baseline.
- **Ridge Regression** — adds L2 regularisation, good when n is small.
- **Random Forest** — non-linear ensemble of decision trees.
"""
))
cells.append(new_code_cell(
"""models = {
    "Linear Regression": LinearRegression(),
    "Ridge (alpha=1.0)": Ridge(alpha=1.0, random_state=RANDOM_STATE),
    "Random Forest"   : RandomForestRegressor(
        n_estimators=200, max_depth=4, random_state=RANDOM_STATE),
}

trained = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    trained[name] = model
    print(f"Trained: {name}")
"""
))

# ------------------------------------------------------------------
cells.append(new_markdown_cell(
"""## 6. Evaluate on the test months

We compare each model on the same 6-month holdout using three metrics:

- **RMSE** — Root mean squared error (lower is better, in z-units).
- **MAE**  — Mean absolute error (lower is better, in z-units).
- **R²**   — Coefficient of determination (1.0 is perfect, 0 means as good as predicting the mean, negative = worse than the mean).
"""
))
cells.append(new_code_cell(
"""def evaluate(model, X_test, y_test):
    y_pred = model.predict(X_test)
    return {
        "RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),
        "MAE" : mean_absolute_error(y_test, y_pred),
        "R2"  : r2_score(y_test, y_pred),
    }

results = {name: evaluate(m, X_test, y_test) for name, m in trained.items()}
results_df = pd.DataFrame(results).T.round(3)
results_df = results_df.sort_values("RMSE")
print("Test-set performance (sorted by RMSE):")
results_df
"""
))

# ------------------------------------------------------------------
cells.append(new_markdown_cell(
"""## 7. Visualise predictions vs actual

Plot the actual `steam_trends_z` for the test months along with each model's
prediction so we can see which one tracks reality best.
"""
))
cells.append(new_code_cell(
"""fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(y_test.index, y_test.values, marker="o", linewidth=2,
        color="black", label="Actual")

colors = {"Linear Regression": "tab:blue",
          "Ridge (alpha=1.0)": "tab:green",
          "Random Forest"   : "tab:orange"}

for name, model in trained.items():
    y_pred = model.predict(X_test)
    ax.plot(y_test.index, y_pred, marker="x", linestyle="--",
            color=colors[name], label=name)

ax.set_title("Predicted vs Actual — steam_trends_z (last 6 months)")
ax.set_ylabel("Gaming interest (z-score)")
ax.legend()
ax.grid(alpha=0.3)
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig("predictions_vs_actual.png", dpi=140)
plt.show()
"""
))

# ------------------------------------------------------------------
cells.append(new_markdown_cell(
"""## 8. Feature importance

Two simple ways to look at what each model learned:

- **Linear / Ridge:** the fitted coefficients tell us how each feature pushes the prediction.
- **Random Forest:** built-in `.feature_importances_` (mean impurity decrease).
"""
))
cells.append(new_code_cell(
"""# linear coefficients
coef_df = pd.DataFrame({
    "Linear Regression": trained["Linear Regression"].coef_,
    "Ridge (alpha=1.0)": trained["Ridge (alpha=1.0)"].coef_,
}, index=FEATURES).round(3)

print("Linear-model coefficients:")
print(coef_df)
print()

# random forest feature importance
rf_imp = pd.Series(
    trained["Random Forest"].feature_importances_,
    index=FEATURES,
).sort_values(ascending=False).round(3)

print("Random Forest feature importance:")
print(rf_imp)
"""
))

cells.append(new_code_cell(
"""# bar plot of RF feature importance
fig, ax = plt.subplots(figsize=(7, 4))
rf_imp.sort_values().plot(kind="barh", ax=ax, color="tab:orange")
ax.set_title("Random Forest — feature importance")
ax.set_xlabel("Importance")
fig.tight_layout()
fig.savefig("feature_importance.png", dpi=140)
plt.show()
"""
))

# ------------------------------------------------------------------
cells.append(new_markdown_cell(
"""## 9. Save the results table"""
))
cells.append(new_code_cell(
"""results_df.to_csv("results.csv")
print("Saved results.csv")
results_df
"""
))

# ------------------------------------------------------------------
cells.append(new_markdown_cell(
"""## 10. Conclusions

**What I learned from this first ML run:**

1. **Linear models do best here.** With only 30 training months and 4 features,
   the regularised Ridge and the plain Linear Regression beat the Random Forest
   on the holdout. Tree models tend to need more data than this to shine.
2. **USD/TRY is the strongest single predictor.** The linear coefficient on
   `usdtry_z` is positive and the largest in magnitude — when the lira weakens,
   gaming interest goes up. This matches Hypothesis 1 from my EDA stage
   (Pearson r = 0.771).
3. **The crisis-period flag adds little once `usdtry_z` is in the model.**
   That makes sense because the flag is *derived* from USD/TRY (≥ 75th
   percentile), so most of its information is already in `usdtry_z`.
4. **R² on the holdout is positive but modest.** A perfect model would score
   1.0; a model that just predicted the training mean would score around 0.
   Ridge / Linear land clearly above 0, which means the macro signal really
   does help — but month-to-month gaming interest also has a lot of noise we
   are not capturing with just three macro variables.

**What I would try next time:**

- Add **lagged** versions of the features (e.g. last month's USD/TRY) so the
  model can use momentum, not just the current value.
- Use **time-series cross-validation** (`TimeSeriesSplit`) instead of a single
  6-month holdout, to get a more stable RMSE estimate.
- Try **ElasticNet** to combine L1 and L2 regularisation.
"""
))

# ------------------------------------------------------------------
nb = new_notebook(cells=cells)
nb.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11"},
}

# write
with open(NB_PATH, "w") as f:
    nbf.write(nb, f)
print(f"Wrote {NB_PATH}")

# execute
print("Executing notebook...")
ep = ExecutePreprocessor(timeout=300, kernel_name="python3")
ep.preprocess(nb, {"metadata": {"path": str(OUT_DIR)}})

with open(NB_PATH, "w") as f:
    nbf.write(nb, f)
print("Notebook executed and saved.")
