"""
DSA210 - Digital Escapism & Socio-Economic Stress Analysis
Data Processing & Merging Script
Student: Ali Efe Okudan (ID: 34314)
"""

import pandas as pd
import numpy as np


def load_all():
    """Load all collected CSVs and return a dict of DataFrames."""
    dfs = {}

    # Steam CS2
    df = pd.read_csv("steam_cs2_clean.csv", index_col=0, parse_dates=True)
    dfs["steam"] = df["players"].rename("steam_players")

    # USD/TRY
    df = pd.read_csv("usdtry_2023_2025.csv", index_col=0, parse_dates=True)
    dfs["usdtry"] = df["usdtry"]

    # BIST100
    df = pd.read_csv("bist100_2023_2025.csv", index_col=0, parse_dates=True)
    dfs["bist100"] = df["bist100"]

    # Google Trends (may be empty)
    df = pd.read_csv("google_trends_TR.csv", index_col=0, parse_dates=True)
    if not df.empty:
        dfs["trends"] = df
    else:
        dfs["trends"] = None

    return dfs


def resample_monthly(series: pd.Series) -> pd.Series:
    """Resample a daily series to month-end means."""
    return series.resample("ME").mean()


def build_merged(dfs: dict) -> pd.DataFrame:
    """Merge all series into a single monthly DataFrame."""
    monthly = {}

    monthly["steam_players"] = resample_monthly(dfs["steam"])
    monthly["usdtry"]        = resample_monthly(dfs["usdtry"])
    monthly["bist100"]       = resample_monthly(dfs["bist100"])

    merged = pd.DataFrame(monthly)

    if dfs["trends"] is not None and not dfs["trends"].empty:
        trends_monthly = dfs["trends"].resample("ME").mean()
        # Create composite stress index
        stress_cols = [c for c in ["ekonomik kriz", "enflasyon", "dolar kur", "işsizlik"]
                       if c in trends_monthly.columns]
        if stress_cols:
            merged["stress_index"] = trends_monthly[stress_cols].mean(axis=1)
        steam_cols = [c for c in ["cs2", "counter strike", "steam"]
                      if c in trends_monthly.columns]
        if steam_cols:
            merged["steam_trends"] = trends_monthly[steam_cols].mean(axis=1)

    return merged


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing values and detect outliers."""
    # Forward-fill then backward-fill
    df = df.ffill().bfill()

    # IQR-based outlier report (no removal — just flag)
    outlier_counts = {}
    for col in df.columns:
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        n = ((df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)).sum()
        outlier_counts[col] = n
    print("  Outliers detected (IQR):", outlier_counts)

    return df


def add_zscore(df: pd.DataFrame) -> pd.DataFrame:
    """Add z-score normalised columns (suffix _z)."""
    for col in df.columns:
        df[f"{col}_z"] = (df[col] - df[col].mean()) / df[col].std()
    return df


def add_crisis_flag(df: pd.DataFrame, col: str = "usdtry", percentile: float = 0.75) -> pd.DataFrame:
    """Flag months where usdtry > 75th percentile as 'crisis'."""
    threshold = df[col].quantile(percentile)
    df["crisis_period"] = (df[col] >= threshold).astype(int)
    print(f"  Crisis threshold ({int(percentile*100)}th pct of {col}): {threshold:.2f}")
    print(f"  Crisis months: {df['crisis_period'].sum()} / {len(df)}")
    return df


def main():
    print("Loading data...")
    dfs = load_all()

    print("Merging to monthly frequency...")
    merged = build_merged(dfs)
    print(f"  Shape before cleaning: {merged.shape}, date range: {merged.index.min()} → {merged.index.max()}")

    print("Cleaning (fill + outlier report)...")
    merged = clean(merged)

    print("Adding z-score columns...")
    merged = add_zscore(merged)

    print("Adding crisis flag...")
    merged = add_crisis_flag(merged)

    merged.to_csv("merged_dataset.csv")
    print(f"\nSaved merged_dataset.csv  ({len(merged)} rows, {len(merged.columns)} cols)")
    print("Columns:", list(merged.columns))
    return merged


if __name__ == "__main__":
    main()
