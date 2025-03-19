import yfinance as yf 
import pandas as pd 

stock = "AAPL"
data = yf.download(stock, start="2022-01-01", end="2024-01-01")

data.to_csv("AAPL_data.csv")

print(data.head())

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
plt.plot(data['Close'], label="Closing Price", color='blue')
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.title(f"{stock} Stock Price Over Time")
plt.legend()
plt.savefig("stock_plot.png")
print("Chart saved as stock_plot.png")


#Adding moving averages

