from app.game.market import Market
from app.game.news import News
from datetime import datetime, timedelta

# Define game parameters
INITIAL_PRICE = 100.0
INITIAL_VOLATILITY = 0.25
STRIKES = [90, 95, 100, 105, 110]
EXPIRATIONS = [datetime.now() + timedelta(days=30), datetime.now() + timedelta(days=60)]
ROUNDS = 5

def get_player_input(market):
    """
    Get player inputs for bid and ask prices for specific options.
    """
    print("\nOption Chain:")
    print(market.option_chain.to_string(index=False))

    # Get player's inputs
    strike = int(input("\nEnter the strike price for your quote: "))
    option_type = input("Enter option type ('call' or 'put'): ").lower()
    bid = float(input("Enter your bid price: "))
    ask = float(input("Enter your ask price: "))

    # Update market quotes
    market.option_chain.loc[
        (market.option_chain["strike"] == strike) & (market.option_chain["type"] == option_type),
        ["bid_price", "ask_price"]
    ] = [bid, ask]

def simulate_order_flow(market):
    """
    Simulate random client orders and match them with player quotes.
    """
    # Simulate order flow and match quotes (simplified example)
    filled_orders = []

    for _, option in market.option_chain.iterrows():
        # Randomly decide if orders fill at bid or ask prices
        buy_volume = int(option["ask_price"] * 10 * random.random())  # Example: Clients buy at ask
        sell_volume = int(option["bid_price"] * 10 * random.random())  # Example: Clients sell at bid

        filled_orders.append({
            "strike": option["strike"],
            "type": option["type"],
            "buy_volume": buy_volume,
            "sell_volume": sell_volume
        })

    return filled_orders

def calculate_pnl(filled_orders, market):
    """
    Calculate P&L based on filled orders and updated market prices.
    """
    pnl = 0.0

    for order in filled_orders:
        strike = order["strike"]
        option_type = order["type"]
        buy_volume = order["buy_volume"]
        sell_volume = order["sell_volume"]

        # Find the corresponding option in the market
        option = market.option_chain.loc[
            (market.option_chain["strike"] == strike) & (market.option_chain["type"] == option_type)
        ]

        # P&L from bid/ask spread
        bid_price = option["bid_price"].values[0]
        ask_price = option["ask_price"].values[0]
        pnl += sell_volume * bid_price
        pnl -= buy_volume * ask_price

    return pnl

def run_game():
    """
    Main game loop for the ClosedAI Market Making Game.
    """
    # Initialize the market
    market = Market(initial_price=INITIAL_PRICE, volatility=INITIAL_VOLATILITY, expirations=EXPIRATIONS, strikes=STRIKES)

    print("Welcome to the ClosedAI Market Making Game!")
    print("Your goal is to maximize your P&L over 5 rounds by quoting bid/ask prices.")

    total_pnl = 0.0

    for round_num in range(1, ROUNDS + 1):
        print(f"\n--- Round {round_num} ---")

        # Display initial market conditions
        print(f"Stock Price: {market.get_underlying_price()}")
        if market.news_manager.latest_news:
            print(f"News Event: {market.news_manager.latest_news['headline']}")
        else:
            print("News Event: None")

        # Show option chain and get player input
        get_player_input(market)

        # Simulate the round
        market.update_market()  # Updates the market (e.g., stock price, option prices, news impacts)
        filled_orders = simulate_order_flow(market)

        # Calculate round P&L
        round_pnl = calculate_pnl(filled_orders, market)
        total_pnl += round_pnl

        # Display results
        print("\n--- Round Results ---")
        print(f"Updated Stock Price: {market.get_underlying_price()}")
        print("Option Chain:")
        print(market.option_chain.to_string(index=False))
        print(f"Round P&L: {round_pnl:.2f}")
        print(f"Total P&L: {total_pnl:.2f}")

    # End of game summary
    print("\n--- Game Over ---")
    print(f"Your final P&L: {total_pnl:.2f}")

if __name__ == "__main__":
    run_game()
