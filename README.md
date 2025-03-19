# Trading Simulator
# Trading Simulator

## 📌 Overview
This is a **Trading Simulator** for backtesting trading strategies using historical stock data. It leverages **Yahoo Finance (yfinance)** to fetch data and **Backtrader** for strategy implementation. The simulator includes visualization of **moving averages** and **buy/sell signals**.

## 🚀 Features
- Fetches stock price data using `yfinance`
- Computes **50-day & 200-day moving averages**
- Implements **SMA crossover strategy**
- Generates **buy/sell trading signals**
- Saves trading charts for analysis
- Simulates trading to calculate **profit/loss**

## 🛠️ Installation
Ensure you have **Python 3.8+** and install the required dependencies:

```bash
pip install -r requirements.txt
```
If `yfinance` and `backtrader` are missing from your package manager (e.g., `pacman` on Arch Linux), install them via `pip`:

```bash
pip install yfinance backtrader
```

## 📈 Usage
Run the script to simulate trading on a chosen stock:

```bash
python TRADING-SIMULATOR.py
```

### 📊 Example Output
```
Fetching AAPL stock data...
[*********************100%***********************]  1 of 1 completed
Chart saved as Trading_Signals.png
Initial Balance: $10000.00
Final Balance: $12050.00
Net Profit: $2050.00
```

## 🐛 Troubleshooting
### **TypeError: unsupported format string passed to Series.__format__**
- This occurs when trying to format a **Series** instead of a single value.
- **Fix:** Ensure you extract a scalar value before formatting:

```python
print(f"BUY: {current_date.date()} at ${current_price.iloc[-1]:.2f}, Shares: {shares:.2f}, Balance: ${balance:.2f}")
```

## 📜 License
This project is open-source under the **MIT License**.

## 👨‍💻 Author
Developed by **hadasaab** for the **IMC Prosperity Challenge**.

---
✅ **Happy Trading!** 📊🚀

