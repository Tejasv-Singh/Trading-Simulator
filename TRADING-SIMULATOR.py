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

 
data['SMA_50'] = data['Close'].rolling(window=50).mean()
data['SMA_200'] = data['Close'].rolling(window=200).mean()

plt.figure(figsize=(12,6))
plt.plot(data['Close'], label="Closing Price", color='blue', alpha=0.6)
plt.plot(data['SMA_50'], label="50-day SMA", linestyle="dashed", color='green')
plt.plot(data['SMA_200'], label="200-day SMA", linestyle="dashed", color='red')
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.title(f"{stock} Stock Price with Moving Averages")
plt.legend()
plt.savefig("stock_plot_with_moving_averages.png")
print("Chart saved as stock_plot_with_moving_averages.png")



# Define signals
data['Signal'] = 0  # No trade
data.loc[data['SMA_50'] > data['SMA_200'], 'Signal'] = 1  # Buy
data.loc[data['SMA_50'] < data['SMA_200'], 'Signal'] = -1  # Sell

# Ensure 'Trade' column is created if it's used later
data['Trade'] = data['Signal']  # If 'Trade' was intended to store the signals

# Debugging step: Print first few rows to check
print(data.head())

# Plot buy/sell signals
plt.figure(figsize=(12,6))
plt.plot(data['Close'], label="Closing Price", color='blue', alpha=0.6)
plt.plot(data['SMA_50'], label="50-day SMA", linestyle="dashed", color='green')
plt.plot(data['SMA_200'], label="200-day SMA", linestyle="dashed", color='red')

# Ensure data['Trade'] exists before using it in scatter plots
if 'Trade' in data.columns:
    plt.scatter(data.index[data['Trade'] == 1], data['Close'][data['Trade'] == 1],
                label='Buy Signal', marker='^', color='green', alpha=1, edgecolors='black')
    plt.scatter(data.index[data['Trade'] == -1], data['Close'][data['Trade'] == -1],
                label='Sell Signal', marker='v', color='red', alpha=1, edgecolors='black')

plt.legend()
plt.title("Trading Signals Based on SMA Crossovers")
plt.savefig("Trading_Signals_Based_on_SMA_Crossovers.png")
print("Chart saved as Trading_Signals_Based_on_SMA_Crossovers.png")
