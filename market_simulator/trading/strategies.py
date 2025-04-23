import numpy as np
import pandas as pd
# Trading strategies and framework

class TradingStrategy:
    def __init__(self, name):
        self.name = name

    def generate_signals(self, data):
        raise NotImplementedError("Should implement generate_signals()")

class MovingAverageStrategy(TradingStrategy):
    def __init__(self, short_window, long_window):
        super().__init__("Moving Average Strategy")
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        signals['short_mavg'] = data['Close'].rolling(window=self.short_window, min_periods=1, center=False).mean()
        signals['long_mavg'] = data['Close'].rolling(window=self.long_window, min_periods=1, center=False).mean()

        signals['signal'][self.short_window:] = np.where(signals['short_mavg'][self.short_window:] > signals['long_mavg'][self.short_window:], 1.0, 0.0)
        signals['positions'] = signals['signal'].diff()

        return signals

class RSI_Strategy(TradingStrategy):
    def __init__(self, window, overbought, oversold):
        super().__init__("RSI Strategy")
        self.window = window
        self.overbought = overbought
        self.oversold = oversold

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.window).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        signals['rsi'] = rsi
        signals['signal'][rsi > self.overbought] = -1.0
        signals['signal'][rsi < self.oversold] = 1.0
        signals['positions'] = signals['signal'].diff()

        return signals