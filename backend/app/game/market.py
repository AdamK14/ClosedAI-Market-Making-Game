import random
import pandas as pd
from datetime import datetime
from options import Option

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

        # Initialize an empty DataFrame to hold the option chain
        self.option_chain = pd.DataFrame(columns=[
            "strike", "expiration", "type", "theoretical_price", "bid_price", "ask_price"
        ])

        # Generate the initial option chain
        self.generate_option_chain()

    def generate_option_chain(self):
        """
        Generates an initial option chain and populates the DataFrame.
        """
        options = []
        for expiration in self.expirations:
            for strike in self.strikes:
                for option_type in ["call", "put"]:
                    # Use the Option class to calculate theoretical prices
                    option = Option(
                        strike=strike,
                        expiration=expiration,
                        option_type=option_type,
                        underlying_price=self.underlying_price,
                        volatility=self.volatility,
                    )
                    options.append({
                        "strike": strike,
                        "expiration": expiration,
                        "type": option_type,
                        "theoretical_price": option.theoretical_price,
                        "bid_price": option.bid_price,
                        "ask_price": option.ask_price
                    })

        # Convert the list of options to a DataFrame
        self.option_chain = pd.DataFrame(options)

    def update_market(self):
        """
        Updates the underlying price and refreshes the option chain.
        """
        # Simulate a random price movement for the underlying
        self.underlying_price += round(random.uniform(-1, 1), 2)

        # Update each row in the DataFrame with new option prices
        def update_row(row):
            option = Option(
                strike=row["strike"],
                expiration=row["expiration"],
                option_type=row["type"],
                underlying_price=self.underlying_price,
                volatility=self.volatility,
            )
            return pd.Series({
                "theoretical_price": option.theoretical_price,
                "bid_price": option.bid_price,
                "ask_price": option.ask_price
            })

        # Apply the updates to the DataFrame
        updated_data = self.option_chain.apply(update_row, axis=1)
        self.option_chain.update(updated_data)

    def filter_options(self, min_strike=None, max_strike=None, option_type=None):
        """
        Filters the option chain based on criteria.
        Args:
            min_strike (float): Minimum strike price.
            max_strike (float): Maximum strike price.
            option_type (str): Filter by option type ('call' or 'put').

        Returns:
            pd.DataFrame: Filtered DataFrame.
        """
        filtered_chain = self.option_chain
        if min_strike is not None:
            filtered_chain = filtered_chain[filtered_chain["strike"] >= min_strike]
        if max_strike is not None:
            filtered_chain = filtered_chain[filtered_chain["strike"] <= max_strike]
        if option_type is not None:
            filtered_chain = filtered_chain[filtered_chain["type"] == option_type]
        return filtered_chain

    def get_underlying_price(self):
        """
        Returns the current underlying price of ClosedAI stock.
        """
        return self.underlying_price
