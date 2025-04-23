import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import asyncio
import websockets
import json
import numpy as np
from market_simulator.gbm import GeometricBrownianMotion

async def price_stream(websocket, path):
    S0, mu, sigma, T, dt = 100, 0.05, 0.2, 1, 1/252
    price = S0
    while True:
        # Simulate next price using GBM step
        W = np.random.normal(0, np.sqrt(dt))
        price = price * np.exp((mu - 0.5 * sigma**2) * dt + sigma * W)
        await websocket.send(json.dumps({"price": float(price)}))
        await asyncio.sleep(0.1)

async def main():
    async with websockets.serve(price_stream, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())