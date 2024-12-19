import pandas as pd
from datetime import datetime
from app.core.news import News
from app.core.options import Option
import random

class Market:
    def __init__(self, initial_price, volatility, expirations, strikes, refresh_interval=5):
        """
        Initialize the ClosedAI market.
        """
        self.underlying_price = initial_price
        self.volatility = volatility
        self.expirations = expirations
        self.strikes = strikes
        self.refresh_interval = refresh_interval
        self.last_update_time = datetime.now()

        # News manager
        self.news_manager = News()

        # Option chain as a DataFrame
        self.option_chain = pd.DataFrame(columns=[
            "strike", "expiration", "type", "theoretical_price", 
            "bid_price", "ask_price", "delta", "gamma", "vega", "theta", "rho"
        ])

        # Generate the option chain
        self.generate_option_chain()

    def generate_option_chain(self):
        """
        Generates an initial option chain as a Pandas DataFrame.
        """
        options = []
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
                    options.append({
                        "strike": strike,
                        "expiration": expiration,
                        "type": option_type,
                        "theoretical_price": option.theoretical_price,
                        "bid_price": option.bid_price,
                        "ask_price": option.ask_price,
                        "delta": option.delta,
                        "gamma": option.gamma,
                        "vega": option.vega,
                        "theta": option.theta,
                        "rho": option.rho,
                    })

        # Convert the options list to a DataFrame
        self.option_chain = pd.DataFrame(options)

    def update_market(self):
        """
        Updates the underlying price, volatility, and option prices.
        """
        # Simulate price movement
        self.underlying_price += round(random.uniform(-1, 1), 2)

        # Check for news and apply its impact
        current_time = datetime.now()
        news_event = self.news_manager.generate_news(current_time, probability=0.3)
        if news_event:
            self.underlying_price, self.volatility = self.news_manager.apply_news_impact(
                self.underlying_price, self.volatility
            )
            print(f"News Event: {news_event['headline']}")

        # Update all options in the DataFrame
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
                "ask_price": option.ask_price,
                "delta": option.delta,
                "gamma": option.gamma,
                "vega": option.vega,
                "theta": option.theta,
                "rho": option.rho,
            })

        self.option_chain.update(self.option_chain.apply(update_row, axis=1))
