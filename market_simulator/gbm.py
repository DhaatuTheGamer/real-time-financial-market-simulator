import numpy as np

class GeometricBrownianMotion:
    def __init__(self, S0, mu, sigma, T, dt):
        self.S0 = S0
        self.mu = mu
        self.sigma = sigma
        self.T = T
        self.dt = dt
        self.n = int(T / dt)
        self.t = np.linspace(0, T, self.n)
        self.S = np.zeros(self.n)
        self.S[0] = S0

    def simulate(self):
        for i in range(1, self.n):
            W = np.random.normal(0, np.sqrt(self.dt))
            self.S[i] = self.S[i-1] * np.exp((self.mu - 0.5 * self.sigma**2) * self.dt + self.sigma * W)
        return self.S