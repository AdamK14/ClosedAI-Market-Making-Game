from app.game.market import Market
from app.game.player import Player

class RoundManager:
    """
    Manages the game rounds and interactions.
    """
    def __init__(self, market, player, rounds=5):
        self.market = market
        self.player = player
        self.rounds = rounds
        self.current_round = 0

    def start_round(self):
        """
        Starts a new round, displaying market conditions and collecting player input.
        """
        self.current_round += 1
        print(f"\n--- Round {self.current_round} ---")
        print(f"Stock Price: {self.market.get_underlying_price()}")
        if self.market.news_manager.latest_news:
            print(f"News Event: {self.market.news_manager.latest_news['headline']}")
        else:
            print("News Event: None")
        print("\nOption Chain:")
        print(self.market.option_chain.to_string(index=False))

    def process_player_input(self):
        """
        Collects and processes player input for bid/ask quotes.
        """
        strike = int(input("\nEnter the strike price for your quote: "))
        option_type = input("Enter option type ('call' or 'put'): ").lower()
        bid = float(input("Enter your bid price: "))
        ask = float(input("Enter your ask price: "))

        self.market.option_chain.loc[
            (self.market.option_chain["strike"] == strike) &
            (self.market.option_chain["type"] == option_type),
            ["bid_price", "ask_price"]
        ] = [bid, ask]

    def simulate_round(self):
        """
        Simulates the round by updating the market and calculating P&L.
        """
        self.market.update_market()
        filled_orders = simulate_order_flow(self.market)
        round_pnl = calculate_pnl(filled_orders, self.market)
        self.player.total_pnl += round_pnl
        print("\n--- Round Results ---")
        print(f"Updated Stock Price: {self.market.get_underlying_price()}")
        print("Option Chain:")
        print(self.market.option_chain.to_string(index=False))
        print(f"Round P&L: {round_pnl:.2f}")
        print(f"Total P&L: {self.player.total_pnl:.2f}")

    def play_game(self):
        """
        Runs the game for the specified number of rounds.
        """
        for _ in range(self.rounds):
            self.start_round()
            self.process_player_input()
            self.simulate_round()
        print("\n--- Game Over ---")
        print(f"Final Total P&L: {self.player.total_pnl:.2f}")
