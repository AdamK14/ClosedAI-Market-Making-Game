class Player:
    """
    Represents a player in the ClosedAI Market Making Game.
    Tracks inventory, cash, and P&L.
    """
    def __init__(self):
        self.cash = 0.0  # Total cash balance
        self.inventory = {}  # Tracks options and underlying stock positions (by option key)
        self.total_pnl = 0.0  # Total profit and loss

    def update_inventory(self, option_key, quantity, price):
        """
        Updates the player's inventory after a trade.
        Args:
            option_key (dict): A unique key for the option (e.g., {"strike": 100, "expiration": "2024-12-31", "type": "call"}).
            quantity (int): Number of options bought/sold (positive for buy, negative for sell).
            price (float): Price per option.
        """
        key_tuple = tuple(option_key.items())  # Convert dict to hashable tuple for inventory tracking
        if key_tuple not in self.inventory:
            self.inventory[key_tuple] = {"quantity": 0, "cost_basis": 0.0}
        
        # Update inventory
        self.inventory[key_tuple]["quantity"] += quantity
        self.inventory[key_tuple]["cost_basis"] += quantity * price
        self.cash -= quantity * price

    def calculate_inventory_pnl(self, market):
        """
        Calculates the P&L from the player's inventory based on current market prices.
        Args:
            market (Market): The market instance for accessing updated option prices.
        """
        pnl = 0.0
        for option_key, position in self.inventory.items():
            quantity = position["quantity"]
            key_dict = dict(option_key)  # Convert tuple back to dict
            strike = key_dict["strike"]
            expiration = key_dict["expiration"]
            option_type = key_dict["type"]
            
            # Retrieve the market price for the option
            try:
                option = market.option_chain.loc[
                    (market.option_chain["Strike Price"] == strike) &
                    (market.option_chain["Expiration"] == expiration) &
                    (market.option_chain["Type"] == option_type)
                ]
                market_price = option["Call LTP"].values[0] if option_type == "call" else option["Put LTP"].values[0]
                pnl += quantity * market_price
            except IndexError:
                # Option not found in the market (e.g., expired)
                continue
        return pnl

    def get_total_pnl(self, market):
        """
        Calculates the total P&L (cash + inventory valuation).
        Args:
            market (Market): The market instance for accessing updated option prices.
        """
        inventory_pnl = self.calculate_inventory_pnl(market)
        return self.cash + inventory_pnl

    def display_inventory(self):
        """
        Displays the player's current inventory and cash balance.
        """
        print(f"Cash Balance: {self.cash:.2f}")
        print("Inventory:")
        for option_key, position in self.inventory.items():
            key_dict = dict(option_key)
            print(f"Option: {key_dict}, Quantity: {position['quantity']}, Cost Basis: {position['cost_basis']:.2f}")