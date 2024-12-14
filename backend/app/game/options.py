import math
from scipy.stats import norm

class Option:
    """
    Represents a single option contract.
    """
    def __init__(self, strike, expiration, option_type, underlying_price, volatility, risk_free_rate=0.01):
        """
        Initialize an option.
        Args:
            strike (float): Strike price of the option.
            expiration (datetime): Expiration date of the option.
            option_type (str): Type of the option ('call' or 'put').
            underlying_price (float): Current price of the underlying stock.
            volatility (float): Implied volatility of the option.
            risk_free_rate (float): Risk-free interest rate (default 1%).
        """
        self.strike = strike
        self.expiration = expiration
        self.option_type = option_type
        self.underlying_price = underlying_price
        self.volatility = volatility
        self.risk_free_rate = risk_free_rate

        # Placeholder for market data
        self.theoretical_price = None
        self.bid_price = None
        self.ask_price = None

        # Calculate initial prices
        self.update_prices()

    def time_to_expiration(self):
        """
        Calculates time to expiration in years.
        """
        from datetime import datetime
        delta = self.expiration - datetime.now()
        return max(delta.days / 365.0, 0.001)  # Prevent division by zero

    def calculate_theoretical_price(self):
        """
        Calculates the theoretical price using the Black-Scholes model.
        """
        T = self.time_to_expiration()
        S = self.underlying_price
        K = self.strike
        r = self.risk_free_rate
        sigma = self.volatility

        d1 = (math.log(S / K) + (r + (sigma ** 2) / 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        if self.option_type == "call":
            price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
        elif self.option_type == "put":
            price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        else:
            raise ValueError("Invalid option type. Must be 'call' or 'put'.")
        
        return max(price, 0)  # Prevent negative prices

    def update_prices(self):
        """
        Updates the theoretical price and sets bid/ask prices.
        """
        self.theoretical_price = self.calculate_theoretical_price()
        self.bid_price = round(self.theoretical_price * 0.95, 2)  # Example bid price
        self.ask_price = round(self.theoretical_price * 1.05, 2)  # Example ask price

    def get_summary(self):
        """
        Returns a dictionary summarizing the option's current data.
        """
        return {
            "strike": self.strike,
            "expiration": self.expiration.strftime("%Y-%m-%d"),
            "type": self.option_type,
            "theoretical_price": self.theoretical_price,
            "bid_price": self.bid_price,
            "ask_price": self.ask_price,
        }
