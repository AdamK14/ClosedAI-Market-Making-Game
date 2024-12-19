import unittest
from datetime import datetime
from  core.news import News

class TestNews(unittest.TestCase):
    def setUp(self):
        """
        Set up the News instance for testing.
        """
        self.news_manager = News()
        self.initial_price = 100.0
        self.initial_volatility = 0.25

    def test_generate_news_probability(self):
        """
        Test that news is generated based on probability.
        """
        news = self.news_manager.generate_news(datetime.now(), probability=1.0)  # Force generation
        self.assertIsNotNone(news, "News should be generated when probability is 1.0")
        self.assertIn("headline", news, "Generated news should have a headline")
        self.assertIn("impact", news, "Generated news should have an impact")

    def test_no_news_on_low_probability(self):
        """
        Test that no news is generated with low probability.
        """
        news = self.news_manager.generate_news(datetime.now(), probability=0.0)  # Force no generation
        self.assertIsNone(news, "No news should be generated when probability is 0.0")

    def test_unique_news_events(self):
        """
        Test that no duplicate news events occur during the game.
        """
        used_headlines = set()
        for _ in range(len(self.news_manager.news_events)):
            news = self.news_manager.generate_news(datetime.now(), probability=1.0)  # Always generate
            self.assertIsNotNone(news, "News should be generated")
            headline = news["headline"]
            self.assertNotIn(headline, used_headlines, f"Duplicate news headline found: {headline}")
            used_headlines.add(headline)
        
        # Ensure no news left after all unique events are used
        news = self.news_manager.generate_news(datetime.now(), probability=1.0)
        self.assertIsNone(news, "No news should be generated after all events are used")

    def test_apply_news_impact(self):
        """
        Test that news impact correctly modifies price and volatility.
        """
        news = self.news_manager.generate_news(datetime.now(), probability=1.0)
        self.assertIsNotNone(news, "News should be generated for impact testing")

        updated_price, updated_volatility = self.news_manager.apply_news_impact(self.initial_price, self.initial_volatility)
        
        # Check that the price and volatility are modified
        price_multiplier = news["impact"]["price_multiplier"]
        volatility_change = news["impact"]["volatility_change"]

        expected_price = round(self.initial_price * price_multiplier, 2)
        expected_volatility = max(0.01, self.initial_volatility + volatility_change)

        self.assertEqual(updated_price, expected_price, "Price impact is incorrect")
        self.assertAlmostEqual(updated_volatility, expected_volatility, places=5, msg="Volatility impact is incorrect")

    def test_clear_news(self):
        """
        Test that clearing the news resets the latest news.
        """
        self.news_manager.generate_news(datetime.now(), probability=1.0)
        self.assertIsNotNone(self.news_manager.latest_news, "News should exist before clearing")

        self.news_manager.clear_news()
        self.assertIsNone(self.news_manager.latest_news, "Latest news should be cleared")

if __name__ == "__main__":
    unittest.main()
