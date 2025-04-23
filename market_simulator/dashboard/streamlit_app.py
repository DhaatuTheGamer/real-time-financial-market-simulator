import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
import numpy as np
from market_simulator.gbm import GeometricBrownianMotion
from market_simulator.trading.strategies import MovingAverageStrategy, RSI_Strategy
from market_simulator.trading.backtester import Backtester
from market_simulator.data.alpha_vantage import AlphaVantage
import asyncio
import websockets
import json

def run_websocket_client(uri, n_points=100):
    prices = []
    async def get_prices():
        async with websockets.connect(uri) as websocket:
            for _ in range(n_points):
                msg = await websocket.recv()
                data = json.loads(msg)
                prices.append(data["price"])
    try:
        asyncio.run(get_prices())
    except RuntimeError:
        # For Streamlit reruns, use a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(get_prices())
    return prices

def main():
    st.title("Real-Time Financial Market Simulator")
    st.sidebar.header("GBM Parameters")
    S0 = st.sidebar.number_input("Initial Price (S0)", value=100.0)
    mu = st.sidebar.number_input("Drift (mu)", value=0.05)
    sigma = st.sidebar.number_input("Volatility (sigma)", value=0.2)
    T = st.sidebar.number_input("Time Horizon (years, T)", value=1.0)
    dt = st.sidebar.number_input("Time Step (dt)", value=1/252.0, format="%0.6f")

    st.sidebar.header("Trading Strategy")
    strategy_type = st.sidebar.selectbox("Select Strategy", ["None", "Moving Average", "RSI"])

    st.sidebar.header("Data Source")
    data_source = st.sidebar.selectbox("Select Data Source", ["Simulated (GBM)", "Alpha Vantage"])
    av_symbol = st.sidebar.text_input("Alpha Vantage Symbol", value="AAPL")
    av_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    av_data = None
    if data_source == "Alpha Vantage" and st.sidebar.button("Fetch Alpha Vantage Data"):
        av = AlphaVantage(api_key=av_api_key)
        av_data_json = av.get_stock_data(av_symbol)
        # Try to extract daily close prices
        try:
            time_series = av_data_json['Time Series (Daily)']
            av_data = pd.DataFrame({
                'Close': [float(v['4. close']) for v in time_series.values()]
            }, index=pd.to_datetime(list(time_series.keys())))
            av_data = av_data.sort_index()
            st.success(f"Fetched {len(av_data)} data points for {av_symbol}")
            st.line_chart(av_data['Close'])
        except Exception as e:
            st.error(f"Failed to parse Alpha Vantage data: {e}")

    # Real-time price streaming (WebSocket)
    st.sidebar.header("Real-Time Streaming")
    if st.sidebar.button("Start Real-Time Stream"):
        st.info("Open a new terminal and run: python market_simulator/websocket_server.py")
        st.info("Then use a WebSocket client to connect to ws://localhost:8765")
        st.warning("Streamlit cannot natively receive WebSocket data in real time, but you can visualize streamed data with a custom client.")

    ws_enabled = st.sidebar.checkbox("Visualize Real-Time WebSocket Prices")
    ws_uri = st.sidebar.text_input("WebSocket URI", value="ws://localhost:8765")
    n_points = st.sidebar.number_input("Points to Stream", value=100, min_value=1)
    if ws_enabled and st.button("Start WebSocket Stream"):
        st.info(f"Connecting to {ws_uri} and streaming {n_points} price points...")
        prices = run_websocket_client(ws_uri, n_points)
        st.line_chart(prices)
        st.write(f"Received {len(prices)} streamed prices.")

    # Main simulation/backtest logic
    if st.button("Simulate/Run Backtest"):
        if data_source == "Alpha Vantage" and av_data is not None:
            df = av_data.copy()
        else:
            gbm = GeometricBrownianMotion(S0, mu, sigma, T, dt)
            prices = gbm.simulate()
            df = pd.DataFrame({"Close": prices})
        st.line_chart(df["Close"])
        st.write(f"Loaded {len(df)} price points.")

        signals = None
        if strategy_type == "Moving Average":
            short_window = st.sidebar.number_input("Short Window", value=10, min_value=1)
            long_window = st.sidebar.number_input("Long Window", value=30, min_value=1)
            strategy = MovingAverageStrategy(short_window, long_window)
            signals = strategy.generate_signals(df)
            st.line_chart(signals[["short_mavg", "long_mavg"]])
            st.write(signals.tail())
            backtester = Backtester(strategy, df)
            results = backtester.run_backtest()
            st.write("Backtest results:", results)
        elif strategy_type == "RSI":
            window = st.sidebar.number_input("RSI Window", value=14, min_value=1)
            overbought = st.sidebar.number_input("Overbought Threshold", value=70)
            oversold = st.sidebar.number_input("Oversold Threshold", value=30)
            strategy = RSI_Strategy(window, overbought, oversold)
            signals = strategy.generate_signals(df)
            st.line_chart(signals["rsi"])
            st.write(signals.tail())
            backtester = Backtester(strategy, df)
            results = backtester.run_backtest()
            st.write("Backtest results:", results)
        else:
            results = df

        # Export results
        st.header("Export Results")
        csv = df.to_csv().encode('utf-8')
        st.download_button("Download CSV", csv, "results.csv", "text/csv")
        json_str = df.to_json()
        st.download_button("Download JSON", json_str, "results.json", "application/json")

if __name__ == "__main__":
    main()