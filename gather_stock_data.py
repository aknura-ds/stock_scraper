import yfinance as yf
import pandas as pd

ticker = "^GSPC"

df = yf.download(tickers=ticker, period="7d", interval="1m", progress=False)

df.reset_index(inplace=True)
df.rename(columns={"Datetime": "Date"}, inplace=True)

df["Stock_Price"] = df["Close"]


df.to_csv("all_stock_data.csv", index=False)
print("Data is saved to all_stock_data.csv")
print(df.head())
