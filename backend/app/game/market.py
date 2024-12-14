from options import Option
from datetime import datetime

class Market:
    def __init__(self, initial_price, volatility, expirations, strikes, refresh_interval=5):
        """
        Initialize the ClosedAI market.
        Args:
            initial_price (float): Starting stock price of ClosedAI.
            volatility (float): Initial implied volatility.
            expirations (list): List of expiration dates for options.
            strikes (list): List of strike prices for options.
            refresh_interval (int): Time interval (seconds) for market updates.
        """
        self.underlying_price = initial_price
        self.volatility = volatility
        self.expirations = expirations
        self.strikes = strikes
        self.refresh_interval = refresh_interval
        self.last_update_time = datetime.now()
        self.option_chain = []
        
        self.generate_option_chain()

    def generate_option_chain(self):
        """
        Generates an initial option chain using the Option class.
        """
        for expiration in self.expirations:
            for strike in self.strikes:
                for option_type in ["call", "put"]:
                    option = Option(
                        strike=strike,
                        expiration=expiration,
                        option_type=option_type,
                        underlying_price=self.underlying_price,
                        volatility=self.volatility,
                    )
                    self.option_chain.append(option)

    def update_market(self):
        """
        Updates the underlying price and refreshes all option prices.
        """
        # Simulate price movement
        self.underlying_price += round(random.uniform(-1, 1), 2)

        # Update all options
        for option in self.option_chain:
            option.underlying_price = self.underlying_price
            option.volatility = self.volatility
            option.update_prices()

    def get_option_chain(self):
        """
        Returns the current option chain as a list of summaries.
        """
        return [option.get_summary() for option in self.option_chain]

    def get_underlying_price(self):
        """
        Returns the current underlying price of ClosedAI stock.
        """
        return self.underlying_price
