import pandas as pd

df = pd.read_csv("all_stock_data.csv", parse_dates=["Date"])

df = df.dropna(subset=["Close"])

cols_to_convert = ["Open", "High", "Low", "Close", "Volume"]
for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df.dropna(subset=cols_to_convert, inplace=True)

df["SMA_5"] = df["Close"].rolling(window=5).mean()
df["SMA_15"] = df["Close"].rolling(window=15).mean()

df["EMA_5"] = df["Close"].ewm(span=5, adjust=False).mean()
df["EMA_15"] = df["Close"].ewm(span=15, adjust=False).mean()

df["Return_1"] = df["Close"].pct_change()

df["Volatility_5"] = df["Close"].rolling(window=5).std()

df["Momentum_5"] = df["Close"] - df["Close"].shift(5)

df.dropna(inplace=True)
df.to_csv("all_stock_data_feat.csv", index=False)
print("All features are added to all_stock_data_feat.csv")
print(df.head())