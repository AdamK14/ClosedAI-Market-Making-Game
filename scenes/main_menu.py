import pygame
from scenes.base_scene import BaseScene

class MainMenuScene(BaseScene):
    """
    Main menu scene for the Market Making Game.
    Displays the title and allows the player to start the game or quit.
    """

    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.font_title = pygame.font.Font(None, 64)
        self.font_instruction = pygame.font.Font(None, 36)
        self.title_color = (255, 255, 255)  # White
        self.instruction_color = (200, 200, 200)  # Light gray
        self.background_color = (0, 0, 0)  # Black

    def handle_events(self, events):
        """
        Handle key press events for starting the game or quitting.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game
                    self.stop()  # This stops the scene and transitions to the next one
                elif event.key == pygame.K_ESCAPE:  # Quit the game
                    self.running = False
                    pygame.quit()
                    exit()

    def update(self):
        """
        Update logic for the main menu.
        (No dynamic updates needed for a static menu.)
        """
        pass

    def draw(self):
        """
        Draw the main menu screen.
        """
        self.screen.fill(self.background_color)  # Clear the screen with a black background

        # Render the title and instructions
        title_text = self.font_title.render("Market Making Game", True, self.title_color)
        instruction_text = self.font_instruction.render("Press ENTER to Start", True, self.instruction_color)
        quit_text = self.font_instruction.render("Press ESC to Quit", True, self.instruction_color)

        # Center the title and instructions on the screen
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 200))
        instruction_rect = instruction_text.get_rect(center=(self.screen.get_width() // 2, 300))
        quit_rect = quit_text.get_rect(center=(self.screen.get_width() // 2, 350))

        # Draw the text
        self.screen.blit(title_text, title_rect)
        self.screen.blit(instruction_text, instruction_rect)
        self.screen.blit(quit_text, quit_rect)
