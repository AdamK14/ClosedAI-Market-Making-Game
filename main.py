import pygame
from datetime import datetime, timedelta
from app.core.market import Market
from app.core.player import Player
from app.core.round_manager import RoundManager

# Initialize Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Market Making Game")
clock = pygame.time.Clock()

# Fonts and Colors
FONT = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Initialize game components
market = Market(
    initial_price=100.0,
    volatility=0.25,
    expirations=[datetime.now() + timedelta(days=30), datetime.now() + timedelta(days=60)],
    strikes=[90, 95, 100, 105, 110]
)
player = Player()
round_manager = RoundManager(market, player)


# Scene Base Class
class Scene:
    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


# Main Menu Scene
class MainMenu(Scene):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to start the game
                    return "gameplay"

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BLACK)
        title = FONT.render("Market Making Game", True, WHITE)
        instruction = FONT.render("Press Enter to Start", True, GRAY)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 300))


# Gameplay Scene
class Gameplay(Scene):
    def __init__(self, market, player, round_manager):
        self.market = market
        self.player = player
        self.round_manager = round_manager
        self.message = "Press S to simulate the round, Q to quit."

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Simulate the round
                    self.round_manager.simulate_round()
                    self.message = "Round simulated! Press S again or Q to quit."
                elif event.key == pygame.K_q:  # Quit the game
                    return "results"

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BLACK)
        stock_price = FONT.render(f"Stock Price: {self.market.underlying_price:.2f}", True, WHITE)
        pnl = FONT.render(f"Player P&L: {self.player.total_pnl:.2f}", True, WHITE)
        message = FONT.render(self.message, True, GRAY)
        screen.blit(stock_price, (50, 50))
        screen.blit(pnl, (50, 100))
        screen.blit(message, (50, 150))


# Results Scene
class Results(Scene):
    def __init__(self, player):
        self.player = player

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    return "main_menu"
                elif event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    exit()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BLACK)
        result = FONT.render(f"Final P&L: {self.player.total_pnl:.2f}", True, WHITE)
        instruction = FONT.render("Press R to Restart or Q to Quit", True, GRAY)
        screen.blit(result, (SCREEN_WIDTH // 2 - result.get_width() // 2, 200))
        screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 300))


# Scene Manager
class SceneManager:
    def __init__(self):
        self.scenes = {
            "main_menu": MainMenu(),
            "gameplay": Gameplay(market, player, round_manager),
            "results": Results(player)
        }
        self.current_scene = "main_menu"

    def handle_events(self, events):
        next_scene = self.scenes[self.current_scene].handle_events(events)
        if next_scene:
            self.current_scene = next_scene

    def update(self):
        self.scenes[self.current_scene].update()

    def draw(self, screen):
        self.scenes[self.current_scene].draw(screen)


# Main Game Loop
def main():
    scene_manager = SceneManager()
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Handle events, update, and draw
        scene_manager.handle_events(events)
        scene_manager.update()
        scene_manager.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
