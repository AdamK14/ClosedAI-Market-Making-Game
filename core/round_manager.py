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
        Starts a new round, displaying market conditions and news events.
        """
        self.current_round += 1
        print(f"\n--- Round {self.current_round} ---")
        print(f"Stock Price: {self.market.current_price:.2f}")

        # Display news if available
        if self.market.news.latest_news:
            print(f"News Event: {self.market.news.latest_news['headline']}")
        else:
            print("News Event: None")

        # Display the options chain
        print("\nOption Chain:")
        print(self.market.option_chain.to_string(index=False))

    def process_player_input(self):
        """
        Collects and processes player input for bid/ask quotes or trades.
        """
        while True:
            try:
                strike = int(input("\nEnter the strike price for your trade: "))
                option_type = input("Enter option type ('call' or 'put'): ").lower()
                quantity = int(input("Enter quantity (positive to buy, negative to sell): "))
                price = float(input("Enter your price: "))

                # Update the player's inventory and cash
                option_key = {"strike": strike, "type": option_type, "expiration": "2024-12-31"}
                self.player.update_inventory(option_key, quantity, price)

                print(f"Trade executed: {quantity} {option_type.upper()} options at ${price:.2f}")
                print(f"Updated Cash: ${self.player.cash:.2f}")
                break
            except (ValueError, KeyError):
                print("Invalid input. Please try again.")

    def simulate_round(self):
        """
        Simulates the round by updating the market and calculating P&L.
        """
        # Update the market (includes news-driven price changes)
        self.market.update_market()

        # Calculate player's total P&L
        total_pnl = self.player.get_total_pnl(self.market)

        print("\n--- Round Results ---")
        print(f"Updated Stock Price: {self.market.current_price:.2f}")
        print("Option Chain:")
        print(self.market.option_chain.to_string(index=False))
        print(f"Total P&L: ${total_pnl:.2f}")

    def play_game(self):
        """
        Runs the game for the specified number of rounds.
        """
        print("\n--- Welcome to the Market Making Game ---")
        for _ in range(self.rounds):
            self.start_round()
            self.process_player_input()
            self.simulate_round()

        print("\n--- Game Over ---")
        final_pnl = self.player.get_total_pnl(self.market)
        print(f"Final Total P&L: ${final_pnl:.2f}")
