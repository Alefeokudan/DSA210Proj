"""
DSA210 - Digital Escapism & Socio-Economic Stress Analysis
Data Collection Script
Student: Ali Efe Okudan (ID: 34314)
"""

import time
import pandas as pd
import yfinance as yf

START_DATE = "2023-01-01"
END_DATE   = "2025-12-31"


# ─── 1. USD/TRY ──────────────────────────────────────────────────────────────

def collect_usdtry():
    print("Fetching USD/TRY data...")
    ticker = yf.Ticker("USDTRY=X")
    df = ticker.history(start=START_DATE, end=END_DATE)
    df = df[["Close"]].rename(columns={"Close": "usdtry"})
    df.index = pd.to_datetime(df.index).tz_localize(None)
    df.to_csv("usdtry_2023_2025.csv")
    print(f"  Saved usdtry_2023_2025.csv  ({len(df)} rows)")
    return df


# ─── 2. BIST100 ───────────────────────────────────────────────────────────────

def collect_bist100():
    print("Fetching BIST100 data...")
    ticker = yf.Ticker("XU100.IS")
    df = ticker.history(start=START_DATE, end=END_DATE)
    df = df[["Close"]].rename(columns={"Close": "bist100"})
    df.index = pd.to_datetime(df.index).tz_localize(None)
    df.to_csv("bist100_2023_2025.csv")
    print(f"  Saved bist100_2023_2025.csv  ({len(df)} rows)")
    return df


# ─── 3. Google Trends ─────────────────────────────────────────────────────────

def collect_google_trends():
    print("Fetching Google Trends data...")
    try:
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="tr-TR", tz=180, timeout=(10, 25))

        economic_kw = ["ekonomik kriz", "enflasyon", "dolar kur", "issizlik"]
        steam_kw    = ["cs2", "counter strike", "steam"]

        frames = []
        for kw_group in [economic_kw, steam_kw]:
            time.sleep(30)  # rate-limit guard
            pytrends.build_payload(kw_group, geo="TR", timeframe=f"{START_DATE} {END_DATE}")
            df = pytrends.interest_over_time()
            if "isPartial" in df.columns:
                df = df.drop(columns=["isPartial"])
            frames.append(df)

        result = pd.concat(frames, axis=1)
        result.index = pd.to_datetime(result.index).tz_localize(None)
        result.to_csv("google_trends_TR.csv")
        print(f"  Saved google_trends_TR.csv  ({len(result)} rows, cols: {list(result.columns)})")
        return result

    except Exception as e:
        print(f"  WARNING: Google Trends failed ({e}). Saving empty file.")
        empty = pd.DataFrame(columns=["ekonomik kriz", "enflasyon", "dolar kur", "işsizlik",
                                      "cs2", "counter strike", "steam"])
        empty.to_csv("google_trends_TR.csv")
        return empty


# ─── 4. Steam / SteamDB ───────────────────────────────────────────────────────

def collect_steam():
    print("Loading Steam CS2 data from steamdb_chart_730.csv...")
    df = pd.read_csv("steamdb_chart_730.csv", sep=";")
    df.columns = [c.strip().strip('"') for c in df.columns]

    # Clean DateTime column
    df["DateTime"] = pd.to_datetime(df["DateTime"].str.strip().str.strip('"'), errors="coerce")
    df = df.dropna(subset=["DateTime"])

    # Use Players column; fall back to Average Players where missing
    for col in ["Players", "Average Players"]:
        df[col] = pd.to_numeric(df[col].astype(str).str.strip().str.strip('"'), errors="coerce")

    df["players"] = df["Players"].fillna(df["Average Players"])
    df = df[["DateTime", "players"]].set_index("DateTime")

    # Filter to analysis window
    df = df.loc[START_DATE:END_DATE]
    df.to_csv("steam_cs2_clean.csv")
    print(f"  Saved steam_cs2_clean.csv  ({len(df)} rows)")
    return df


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    collect_usdtry()
    collect_bist100()
    collect_steam()
    collect_google_trends()
    print("\nData collection complete.")
