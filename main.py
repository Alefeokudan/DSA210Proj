import yfinance as yf
import pandas as pd

usdtry = yf.download('USDTRY=X', start='2022-01-01', end='2025-12-31', progress=False)
usdtry = usdtry[['Close']].rename(columns={'Close': 'USDTRY'})
usdtry.to_csv('usdtry.csv')
print(usdtry.tail())