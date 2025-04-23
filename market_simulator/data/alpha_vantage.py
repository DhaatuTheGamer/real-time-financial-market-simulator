# Alpha Vantage API integration

import requests
import os

class AlphaVantage:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('ALPHA_VANTAGE_API_KEY')
        self.base_url = 'https://www.alphavantage.co/query'

    def get_stock_data(self, symbol, function='TIME_SERIES_DAILY'):
        params = {
            'function': function,
            'symbol': symbol,
            'apikey': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data

    def get_forex_data(self, from_currency, to_currency, function='CURRENCY_EXCHANGE_RATE'):
        params = {
            'function': function,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'apikey': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data