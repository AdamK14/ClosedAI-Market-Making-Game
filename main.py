import pygame
from core.market import Market
from core.player import Player
from core.round_manager import RoundManager
from scenes.main_menu import MainMenuScene
from scenes.gameplay import GameplayScene
from scenes.results import ResultsScene

class SceneManager:
    """
    Manages transitions between different scenes in the game.
    """
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.current_scene = None

    def run_scene(self, scene):
        """
        Runs the given scene and manages transitions.
        Args:
            scene (BaseScene): The scene to run.
        """
        self.current_scene = scene
        self.current_scene.run()

    def transition_to(self, scene):
        """
        Transitions to a new scene.
        Args:
            scene (BaseScene): The next scene to run.
        """
        self.run_scene(scene)


def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Market Making Game")

    # Initialize the SceneManager
    scene_manager = SceneManager(screen, clock)

    # Main game loop
    while True:
        # Run the main menu scene
        main_menu = MainMenuScene(screen, clock)
        scene_manager.run_scene(main_menu)

        # Initialize the core game components
        market = Market(
            initial_price=100.0,
            volatility=0.30,
            strikes=[80, 85, 90, 95, 100, 105, 110, 115, 120]
        )
        player = Player()
        round_manager = RoundManager(market, player, rounds=5)

        # Run the gameplay scene
        gameplay = GameplayScene(screen, clock, market, player, round_manager)
        scene_manager.run_scene(gameplay)

        # Run the results scene
        results = ResultsScene(screen, clock, player)
        scene_manager.run_scene(results)


if __name__ == "__main__":
    main()
