import pandas as pd
import numpy as np
from datetime import datetime
from core.news import News

class Market:
    def __init__(self, initial_price, volatility, strikes):
        """
        Initialize the Market with the given parameters.
        """
        self.initial_price = initial_price
        self.current_price = initial_price
        self.volatility = volatility
        self.strikes = strikes
        self.option_chain = self.generate_option_chain()
        self.news = News()

    def generate_option_chain(self):
        """
        Generate a DataFrame representing the options chain for calls and puts.
        Includes random data for Open Interest (OI), Volume, Implied Volatility (IV), etc.
        """
        data = []
        for strike in self.strikes:
            # Simulate data for Calls
            call_iv = round(self.volatility * (1 + abs(strike - self.current_price) / self.current_price), 2)
            call_ltp = max(0, self.current_price - strike) + call_iv * 5  # Example pricing logic
            call_bid_price = round(call_ltp - np.random.uniform(0.1, 0.5), 2)
            call_ask_price = round(call_ltp + np.random.uniform(0.1, 0.5), 2)
            call_oi = np.random.randint(100, 10000)
            call_volume = np.random.randint(1, 1000)

            # Simulate data for Puts
            put_iv = round(self.volatility * (1 + abs(strike - self.current_price) / self.current_price), 2)
            put_ltp = max(0, strike - self.current_price) + put_iv * 5
            put_bid_price = round(put_ltp - np.random.uniform(0.1, 0.5), 2)
            put_ask_price = round(put_ltp + np.random.uniform(0.1, 0.5), 2)
            put_oi = np.random.randint(100, 10000)
            put_volume = np.random.randint(1, 1000)

            # Append row for the options chain
            data.append({
                "Strike Price": strike,
                "Call IV": call_iv,
                "Call LTP": round(call_ltp, 2),
                "Call Bid Price": call_bid_price,
                "Call Ask Price": call_ask_price,
                "Call OI": call_oi,
                "Call Volume": call_volume,
                "Put IV": put_iv,
                "Put LTP": round(put_ltp, 2),
                "Put Bid Price": put_bid_price,
                "Put Ask Price": put_ask_price,
                "Put OI": put_oi,
                "Put Volume": put_volume,
            })

        return pd.DataFrame(data)

    def update_market(self):
        """
        Simulate market movement by updating the stock price and re-pricing the options chain.
        This includes handling news events, if any, or using IV-based price changes.
        """
        # Generate news for this round
        current_time = datetime.now()
        news_event = self.news.generate_news(current_time)

        if news_event:
            print(f"News Event: {news_event['headline']}")
            # Apply news impact to price and volatility
            self.current_price, self.volatility = self.news.apply_news_impact(self.current_price, self.volatility)
            print(f"New Price after News: {self.current_price}, New Volatility: {self.volatility}")
            # Clear the news for subsequent rounds
            self.news.clear_news()
        else:
            # Apply a small IV-based random price change
            price_change = round(np.random.uniform(-1, 1) * self.volatility * 5, 2)
            self.current_price = round(self.current_price + price_change, 2)
            print(f"Price changed by {price_change} based on IV. New Price: {self.current_price}")

        # Update the option chain based on the new stock price
        for index, row in self.option_chain.iterrows():
            strike = row["Strike Price"]

            # Update Call Prices
            call_iv = round(self.volatility * (1 + abs(strike - self.current_price) / self.current_price), 2)
            call_ltp = max(0, self.current_price - strike) + call_iv * 5
            call_bid_price = round(call_ltp - np.random.uniform(0.1, 0.5), 2)
            call_ask_price = round(call_ltp + np.random.uniform(0.1, 0.5), 2)

            self.option_chain.at[index, "Call IV"] = call_iv
            self.option_chain.at[index, "Call LTP"] = round(call_ltp, 2)
            self.option_chain.at[index, "Call Bid Price"] = call_bid_price
            self.option_chain.at[index, "Call Ask Price"] = call_ask_price

            # Update Put Prices
            put_iv = round(self.volatility * (1 + abs(strike - self.current_price) / self.current_price), 2)
            put_ltp = max(0, strike - self.current_price) + put_iv * 5
            put_bid_price = round(put_ltp - np.random.uniform(0.1, 0.5), 2)
            put_ask_price = round(put_ltp + np.random.uniform(0.1, 0.5), 2)

            self.option_chain.at[index, "Put IV"] = put_iv
            self.option_chain.at[index, "Put LTP"] = round(put_ltp, 2)
            self.option_chain.at[index, "Put Bid Price"] = put_bid_price
            self.option_chain.at[index, "Put Ask Price"] = put_ask_price

    def display_option_chain(self):
        """
        Display the options chain in a tabular format for debugging or testing purposes.
        """
        print(f"Underlying Price: {self.current_price}")
        print(self.option_chain.to_string(index=False))

    def get_option_chain(self):
        """
        Return the current options chain as a DataFrame.
        """
        return self.option_chain
