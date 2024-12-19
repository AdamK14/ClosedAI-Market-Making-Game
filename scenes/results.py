import pygame
from scenes.base_scene import BaseScene

class ResultsScene(BaseScene):
    """
    Results scene for the Market Making Game.
    Displays the final results, including the player's total P&L and performance summary.
    """

    def __init__(self, screen, clock, player):
        super().__init__(screen, clock)
        self.player = player
        self.font_title = pygame.font.Font(None, 48)
        self.font_content = pygame.font.Font(None, 36)
        self.background_color = (0, 0, 0)  # Black background
        self.text_color = (255, 255, 255)  # White text
        self.secondary_text_color = (200, 200, 200)  # Light gray text

    def handle_events(self, events):
        """
        Handle key press events to allow restarting the game or quitting.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    self.stop()  # Transition to the main menu or gameplay
                elif event.key == pygame.K_q:  # Quit the game
                    self.running = False
                    pygame.quit()
                    exit()

    def update(self):
        """
        Update logic for the results screen.
        (Static screen; no dynamic updates needed.)
        """
        pass

    def draw(self):
        """
        Render the results screen with the player's final P&L and instructions.
        """
        self.screen.fill(self.background_color)

        # Display title
        title_text = self.font_title.render("Game Over", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)

        # Display final P&L
        final_pnl = self.player.total_pnl
        pnl_text = self.font_content.render(f"Final Total P&L: ${final_pnl:.2f}", True, self.text_color)
        pnl_rect = pnl_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(pnl_text, pnl_rect)

        # Display instructions
        restart_text = self.font_content.render("Press R to Restart", True, self.secondary_text_color)
        quit_text = self.font_content.render("Press Q to Quit", True, self.secondary_text_color)
        restart_rect = restart_text.get_rect(center=(self.screen.get_width() // 2, 300))
        quit_rect = quit_text.get_rect(center=(self.screen.get_width() // 2, 350))
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)
