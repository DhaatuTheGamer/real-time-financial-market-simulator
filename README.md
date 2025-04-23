# Real-Time Financial Market Simulator

A beginner-friendly Python project to simulate and visualize real-time stock prices, test trading strategies, and experiment with real or simulated data.

---

## Features
- **Simulate Stock Prices:** Uses Geometric Brownian Motion (GBM) to generate realistic price paths.
- **Real-Time Streaming:** Streams simulated prices over WebSocket for live visualization.
- **Trading Strategies:** Test built-in strategies (Moving Average, RSI) on any data.
- **Backtesting:** Evaluate strategy performance on historical or simulated data.
- **Streamlit Dashboard:** Easy-to-use web interface for configuration, visualization, and exporting results.
- **Alpha Vantage Integration:** Fetch real-world stock data for analysis and calibration.
- **Export Results:** Download your results as CSV or JSON.

---

## Quick Start

### 1. Clone the Repository
```
git clone <your-repo-url>
cd <project-folder>
```

### 2. Set Up Python Virtual Environment
```
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Add Your Alpha Vantage API Key
- Open `.env` and paste your API key:
  ```
  ALPHA_VANTAGE_API_KEY=your_api_key_here
  ```
- [Get a free API key here.](https://www.alphavantage.co/support/#api-key)

---

## How to Use

### 1. Start the WebSocket Server (for real-time streaming)
Open a terminal in your project root and run:
```
python -m market_simulator.websocket_server
```
This will start streaming simulated prices at `ws://localhost:8765`.

### 2. Launch the Streamlit Dashboard
Open another terminal in your project root and run:
```
streamlit run market_simulator/dashboard/streamlit_app.py
```

### 3. Explore the Dashboard
- **Simulate Prices:** Set GBM parameters and click "Simulate/Run Backtest".
- **Fetch Real Data:** Select "Alpha Vantage" as data source, enter a stock symbol, and fetch data.
- **Test Strategies:** Choose a strategy, set its parameters, and view signals/backtest results.
- **Real-Time Streaming:** Enable "Visualize Real-Time WebSocket Prices" to see live prices.
- **Export:** Download your results as CSV or JSON.

---

## Project Structure
```
market_simulator/
    gbm.py                # GBM simulation logic
    websocket_server.py   # WebSocket server for streaming prices
    utils.py              # Helper functions
    dashboard/
        streamlit_app.py  # Streamlit dashboard
    data/
        alpha_vantage.py  # Alpha Vantage API integration
    trading/
        strategies.py     # Trading strategies
        backtester.py     # Backtesting logic
requirements.txt
.env                      # API keys (not tracked by git)
README.md
```

---

## Troubleshooting
- **ModuleNotFoundError:** Always run commands from the project root directory.
- **WebSocket Connection Issues:** Make sure the server is running before starting the stream in the dashboard.
- **Alpha Vantage Errors:** Check your API key and internet connection.

---

## License
MIT
