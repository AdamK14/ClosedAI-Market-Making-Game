class Player:
    """
    Represents a player in the ClosedAI Market Making Game.
    Tracks inventory, cash, and P&L.
    """
    def __init__(self):
        self.cash = 0.0  # Total cash earned
        self.inventory = {}  # Tracks options and underlying stock positions
        self.total_pnl = 0.0  # Total profit and loss

    def update_inventory(self, option_key, quantity, price):
        """
        Updates the player's inventory after a trade.
        Args:
            option_key (tuple): A unique key for the option (e.g., (strike, expiration, type)).
            quantity (int): Number of options bought/sold.
            price (float): Price per option.
        """
        if option_key not in self.inventory:
            self.inventory[option_key] = 0
        self.inventory[option_key] += quantity
        self.cash -= quantity * price

    def calculate_inventory_pnl(self, market):
        """
        Calculates the P&L from the player's inventory based on current market prices.
        Args:
            market (Market): The market instance for accessing updated option prices.
        """
        pnl = 0.0
        for option_key, quantity in self.inventory.items():
            strike, expiration, option_type = option_key
            option = market.option_chain.loc[
                (market.option_chain["strike"] == strike) &
                (market.option_chain["expiration"] == expiration) &
                (market.option_chain["type"] == option_type)
            ]
            market_price = option["theoretical_price"].values[0]
            pnl += quantity * market_price
        return pnl

    def get_total_pnl(self, market):
        """
        Calculates the total P&L (cash + inventory valuation).
        """
        inventory_pnl = self.calculate_inventory_pnl(market)
        return self.cash + inventory_pnl
