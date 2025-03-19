import yfinance as yf 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Download Apple stock data
stock = "AAPL"
data = yf.download(stock, start="2022-01-01", end="2024-01-01")

# Save raw data to CSV
data.to_csv("AAPL_data.csv")
print(data.head())

# Basic price chart
plt.figure(figsize=(12,6))
plt.plot(data['Close'], label="Closing Price", color='blue')
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.title(f"{stock} Stock Price Over Time")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("stock_plot.png")
print("Chart saved as stock_plot.png")

# Calculate moving averages
# Using shorter timeframes for faster signals
data['SMA_20'] = data['Close'].rolling(window=20).mean()  # Shorter timeframe (20 days instead of 50)
data['SMA_100'] = data['Close'].rolling(window=100).mean()  # Shorter timeframe (100 days instead of 200)

# Generate cleaner signals with fewer false positives
data['Signal'] = 0
# Only generate a signal when a crossover occurs (not for every day)
data.loc[(data['SMA_20'] > data['SMA_100']) & (data['SMA_20'].shift(1) <= data['SMA_100'].shift(1)), 'Signal'] = 1  # Buy signal at crossover
data.loc[(data['SMA_20'] < data['SMA_100']) & (data['SMA_20'].shift(1) >= data['SMA_100'].shift(1)), 'Signal'] = -1  # Sell signal at crossover

# Plot with moving averages
plt.figure(figsize=(12,6))
plt.plot(data['Close'], label="Closing Price", color='blue', alpha=0.6)
plt.plot(data['SMA_20'], label="20-day SMA", linestyle="dashed", color='green')
plt.plot(data['SMA_100'], label="100-day SMA", linestyle="dashed", color='red')
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.title(f"{stock} Stock Price with Moving Averages")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("stock_plot_with_moving_averages.png")
print("Chart saved as stock_plot_with_moving_averages.png")

# Visualizing Buy/Sell Signals
# Find buy and sell points
buy_signals = data[data['Signal'] == 1]
sell_signals = data[data['Signal'] == -1]

# Plot stock price with buy/sell signals
plt.figure(figsize=(12,6))
plt.plot(data['Close'], label="Closing Price", color='blue', alpha=0.6)
plt.plot(data['SMA_20'], label="20-day SMA", linestyle="dashed", color='green')
plt.plot(data['SMA_100'], label="100-day SMA", linestyle="dashed", color='red')

# Plot buy signals (green dots)
plt.scatter(buy_signals.index, buy_signals['Close'], marker="^", color='green', label='Buy Signal', alpha=1, s=100)

# Plot sell signals (red dots)
plt.scatter(sell_signals.index, sell_signals['Close'], marker="v", color='red', label='Sell Signal', alpha=1, s=100)

plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.title(f"{stock} Trading Signals")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("Trading_Signals.png")
print("Chart saved as Trading_Signals.png")

# Simulating Trades and Calculating Profit/Loss
# Improved simulation with position sizing and transaction costs
initial_balance = 10000.0  # Starting money in USD
balance = initial_balance
shares = 0.0  # No shares owned initially
transaction_cost = 0.001  # 0.1% transaction cost

# Create lists to track the equity curve
dates = []
equity = []

# For the first entries, we don't have moving averages yet
data = data.dropna()

# Track all trades
trades = []
current_position = None

for i in range(len(data)):
    current_date = data.index[i]
    # Extract scalar values
    current_price = float(data['Close'].iloc[i])
    current_signal = int(data['Signal'].iloc[i])
    
    # Record equity at each point
    portfolio_value = balance + shares * current_price
    dates.append(current_date)
    equity.append(portfolio_value)
    
    # Check for buy signal
    if current_signal == 1 and shares == 0:  # Buy signal and no position
        # Use only 95% of balance to account for potential price movement
        investment = balance * 0.95
        shares = (investment * (1 - transaction_cost)) / current_price
        balance -= investment
        
        # Record trade
        current_position = {'type': 'buy', 'date': current_date, 'price': current_price, 'shares': shares}
        trades.append(current_position)
        print(f"BUY: {current_date.date()} at ${current_price:.2f}, Shares: {shares:.2f}, Balance: ${balance:.2f}")
        
    # Check for sell signal
    elif current_signal == -1 and shares > 0:  # Sell signal and holding position
        # Calculate proceeds from selling
        proceeds = shares * current_price * (1 - transaction_cost)
        
        # Record trade
        sell_position = {'type': 'sell', 'date': current_date, 'price': current_price, 'shares': shares}
        trades.append(sell_position)
        
        # Calculate profit/loss for this trade
        if current_position:
            profit = proceeds - (current_position['price'] * current_position['shares'])
            trade_return = (current_price / current_position['price'] - 1) * 100
            print(f"SELL: {current_date.date()} at ${current_price:.2f}, Profit: ${profit:.2f}, Return: {trade_return:.2f}%")
            current_position = None
        
        # Update balance
        balance += proceeds
        shares = 0.0
        print(f"New Balance: ${balance:.2f}")

# If we still have shares at the end, calculate their value
if shares > 0:
    final_price = float(data['Close'].iloc[-1])
    balance += shares * final_price * (1 - transaction_cost)
    print(f"FINAL SELL: {data.index[-1].date()} at ${final_price:.2f}, Shares: {shares:.2f}")
    shares = 0.0

# Final portfolio value
final_balance = balance
profit = final_balance - initial_balance
profit_percentage = (profit / initial_balance) * 100

print(f"\nTrading Summary:")
print(f"Initial Balance: ${initial_balance:.2f}")
print(f"Final Balance: ${final_balance:.2f}")
print(f"Net Profit/Loss: ${profit:.2f} ({profit_percentage:.2f}%)")

# Plot equity curve
plt.figure(figsize=(12,6))
plt.plot(dates, equity, label="Portfolio Value", color='purple')
plt.xlabel("Date")
plt.ylabel("Portfolio Value (USD)")
plt.title(f"{stock} Trading Strategy Performance")
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig("Portfolio_Performance.png")
print("Chart saved as Portfolio_Performance.png")

# Calculate performance metrics
if len(dates) > 1:  # Make sure we have enough data points
    # Convert equity to numpy array for calculations
    equity_array = np.array(equity)
    daily_returns = np.diff(equity_array) / equity_array[:-1]
    
    # Calculate annualized return
    annual_return = ((equity[-1] / equity[0]) ** (252 / len(equity)) - 1) * 100
    
    # Calculate maximum drawdown
    max_drawdown = 0
    peak = equity[0]
    for value in equity:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    # Calculate Sharpe ratio (assuming risk-free rate of 0 for simplicity)
    if len(daily_returns) > 0 and np.std(daily_returns) > 0:
        sharpe_ratio = (np.mean(daily_returns) * 252) / (np.std(daily_returns) * np.sqrt(252))
    else:
        sharpe_ratio = 0
    
    print(f"\nPerformance Metrics:")
    print(f"Annualized Return: {annual_return:.2f}%")
    print(f"Maximum Drawdown: {max_drawdown:.2f}%")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Total Number of Trades: {len(trades)}")