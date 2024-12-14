import random

class News:
    """Class to manage unique news events for the game"""
    
    def __init__(self):
        self.news_events = [
            # Bullish news
            {
                "type": "bullish",
                "headline": "ClosedAI unveils a groundbreaking private AI model!",
                "impact": {"price_multiplier_range": (1.03, 1.08), "volatility_change_range": (-0.02, -0.005)}
            },
            {
                "type": "bullish",
                "headline": "Big partnership: ClosedAI joins forces with a global tech giant.",
                "impact": {"price_multiplier_range": (1.07, 1.12), "volatility_change_range": (-0.03, -0.01)}
            },
            {
                "type": "bullish",
                "headline": "Analysts predict ClosedAI to dominate private AI markets.",
                "impact": {"price_multiplier_range": (1.02, 1.05), "volatility_change_range": (-0.01, -0.002)}
            },
            # Bearish news
            {
                "type": "bearish",
                "headline": "ClosedAI's latest release faces unexpected bugs.",
                "impact": {"price_multiplier_range": (0.90, 0.97), "volatility_change_range": (0.01, 0.03)}
            },
            {
                "type": "bearish",
                "headline": "Regulators scrutinize ClosedAI's data privacy practices.",
                "impact": {"price_multiplier_range": (0.85, 0.92), "volatility_change_range": (0.02, 0.05)}
            },
            {
                "type": "bearish",
                "headline": "Competitor unveils an open-source alternative to ClosedAI.",
                "impact": {"price_multiplier_range": (0.93, 0.98), "volatility_change_range": (0.005, 0.02)}
            }
        ]
        self.used_news = []
        self.latest_news = None
        self.last_news_time = None

    def generate_news(self, current_time, probability=0.2):
        """
        Generates a unique news event based on the given probability
        Args:
            current_time (datetime): The current time in the simulation
            probability (float): The chance (0-1) that news will occur in this round

        Returns:
            dict: The generated news event or None if no news occurs
        """
        available_news = [news for news in self.news_events if news not in self.used_news]
        
        if random.random() < probability and available_news:
            news = random.choice(available_news)
            self.used_news.append(news)
            
            # Generate random multipliers and volatility changes
            price_multiplier = random.uniform(*news["impact"]["price_multiplier_range"])
            volatility_change = random.uniform(*news["impact"]["volatility_change_range"])
            
            self.latest_news = {
                "headline": news["headline"],
                "type": news["type"],
                "impact": {"price_multiplier": price_multiplier, "volatility_change": volatility_change},
                "timestamp": current_time
            }
            self.last_news_time = current_time
            return self.latest_news
        return None

    def apply_news_impact(self, current_price, current_volatility):
        """
        Applies the latest news impact on price and volatility
        Args:
            current_price (float): The current stock price
            current_volatility (float): The current stock volatility

        Returns:
            tuple: Updated price and volatility after applying the news impact
        """
        if not self.latest_news:
            return current_price, current_volatility

        impact = self.latest_news["impact"]
        new_price = round(current_price * impact["price_multiplier"], 2)
        new_volatility = max(0.01, current_volatility + impact["volatility_change"])
        return new_price, new_volatility

    def clear_news(self):
        """Clears the latest news after its impact has been applied"""
        self.latest_news = None
