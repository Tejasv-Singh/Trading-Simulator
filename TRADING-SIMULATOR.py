import yfinance as yf 
import pandas as pd 

stock = "AAPL"
data = yf.download(stock, start="2022-01-01", end="2024-01-01")

data.to_csv("AAPL_data.csv")

print(data.head())

