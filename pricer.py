# So what are the parameters that we need for a Black-Scholes pricer? We would need:
#     Current Asset Price (S)
#     Strike Price (K)
#     Time to Expiration (T)
#     Risk-Free Interest Rate (r)
#     Volatility (σ)
#
# We need to implement the formula for the Black-Scholes model using python libraries such as math.log(),
# math.sqrt(), scipy.stats.norm.cdf(), etc.

import math
from scipy.stats import norm
import numpy as np

class BlackScholesPricer:
    def __init__(self, current_asset_price, strike_price, time_to_expiration, risk_free_interest_rate, volatility):
        self.current_asset_price = current_asset_price
        self.strike_price = strike_price
        self.time_to_expiration = time_to_expiration
        self.risk_free_interest_rate = risk_free_interest_rate
        self.volatility = volatility

    def _calculate_d_values(self):
        d1 = (math.log((self.current_asset_price / self.strike_price)) + (self.risk_free_interest_rate + ((self.volatility**2) / 2)) * self.time_to_expiration) / (self.volatility * (math.sqrt(self.time_to_expiration)))
        d2 = d1 - (self.volatility * (math.sqrt(self.time_to_expiration)))
        return d1, d2

    def calculate_call_price(self):
        d1, d2 = self._calculate_d_values()
        call_formula = (self.current_asset_price * norm.cdf(d1)) - self.strike_price * (math.e ** (-self.risk_free_interest_rate * self.time_to_expiration)) * norm.cdf(d2)
        return call_formula

    def calculate_put_price(self):
        d1, d2 = self._calculate_d_values()
        put_formula = self.strike_price * (math.e ** (-self.risk_free_interest_rate * self.time_to_expiration)) * norm.cdf(-d2) - (self.current_asset_price * norm.cdf(-d1))
        return put_formula

pricer = BlackScholesPricer(
    current_asset_price=100.0,
    strike_price=100.0,
    time_to_expiration=1.0,
    risk_free_interest_rate=0.05,
    volatility=0.20
)

print(f"Call Option Price: ${pricer.calculate_call_price():.2f}")
print(f"Put Option Price: ${pricer.calculate_put_price():.2f}")


def generate_heat_map_grid(current_asset_price, strike_price, time_to_expiration, risk_free_interest_rate, volatility, spot_shock_pct=0.20, vol_shock_pct=0.50, grid_points=10, min_vol=0.01):
    spot_min = current_asset_price * (1 - spot_shock_pct)
    spot_max = current_asset_price * (1 + spot_shock_pct)

    spot_prices = np.linspace(spot_min, spot_max, grid_points)

    vol_min = max(min_vol, volatility * (1 - vol_shock_pct))
    vol_max = volatility * (1 + vol_shock_pct)

    vols = np.linspace(vol_min, vol_max, grid_points)

    call_grid = np.zeros((len(vols), len(spot_prices)))
    put_grid = np.zeros((len(vols), len(spot_prices)))

    for i, vol in enumerate(vols):
        for j, spot in enumerate(spot_prices):
            pricer = BlackScholesPricer(
                current_asset_price=spot,
                strike_price=strike_price,
                time_to_expiration=time_to_expiration,
                risk_free_interest_rate=risk_free_interest_rate,
                volatility=vol
            )
            call_grid[i, j] = pricer.calculate_call_price()
            put_grid[i, j] = pricer.calculate_put_price()

    return {
        "spot_prices": spot_prices.tolist(),
        "volatilities": vols.tolist(),
        "call_grid": call_grid.tolist(),
        "put_grid": put_grid.tolist()
    }
