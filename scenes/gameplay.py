import pygame
from scenes.base_scene import BaseScene

class GameplayScene(BaseScene):
    """
    Gameplay scene for the Market Making Game.
    Displays market data, processes player trades, and simulates rounds.
    """

    def __init__(self, screen, clock, market, player, round_manager):
        super().__init__(screen, clock)
        self.market = market
        self.player = player
        self.round_manager = round_manager
        self.font = pygame.font.Font(None, 28)
        self.header_font = pygame.font.Font(None, 36)
        self.background_color = (0, 0, 0)  # Black background
        self.text_color = (255, 255, 255)  # White text

        # State variables
        self.current_message = "Press S to simulate the round, Q to quit."

    def handle_events(self, events):
        """
        Handle player input for the gameplay loop.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Simulate the round
                    self.round_manager.simulate_round()
                    self.current_message = "Round simulated! Press S again or Q to quit."
                elif event.key == pygame.K_q:  # Quit the game
                    self.stop()

    def update(self):
        """
        Update game logic (e.g., market state, player P&L).
        """
        # You can include any periodic updates here if needed
        pass

    def draw(self):
        """
        Render the gameplay screen, including market data, player stats, and messages.
        """
        self.screen.fill(self.background_color)

        # Draw the current stock price
        stock_price_text = self.header_font.render(
            f"Stock Price: ${self.market.current_price:.2f}", True, self.text_color
        )
        self.screen.blit(stock_price_text, (20, 20))

        # Draw the option chain
        options_title = self.header_font.render("Options Chain", True, self.text_color)
        self.screen.blit(options_title, (20, 80))

        y_offset = 120
        for _, row in self.market.option_chain.iterrows():
            option_text = self.font.render(
                f"Strike: {row['Strike Price']} | "
                f"Call Bid: {row['Call Bid Price']} | Call Ask: {row['Call Ask Price']} | "
                f"Put Bid: {row['Put Bid Price']} | Put Ask: {row['Put Ask Price']}",
                True,
                self.text_color,
            )
            self.screen.blit(option_text, (20, y_offset))
            y_offset += 30

        # Draw player stats
        player_cash_text = self.font.render(f"Cash: ${self.player.cash:.2f}", True, self.text_color)
        player_pnl_text = self.font.render(f"Total P&L: ${self.player.get_total_pnl(self.market):.2f}", True, self.text_color)
        self.screen.blit(player_cash_text, (20, y_offset + 20))
        self.screen.blit(player_pnl_text, (20, y_offset + 50))

        # Draw current message
        message_text = self.font.render(self.current_message, True, self.text_color)
        self.screen.blit(message_text, (20, y_offset + 100))
