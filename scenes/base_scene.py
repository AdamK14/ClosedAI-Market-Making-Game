import pygame
from abc import ABC, abstractmethod


class BaseScene(ABC):
    """
    Abstract base class for all scenes in the game.
    Defines the structure for handling events, updating state, and drawing visuals.
    """

    def __init__(self, screen, clock):
        """
        Initialize the scene.
        Args:
            screen (pygame.Surface): The Pygame screen where the scene will be drawn.
            clock (pygame.time.Clock): The clock object to control the frame rate.
        """
        self.screen = screen
        self.clock = clock
        self.running = True

    @abstractmethod
    def handle_events(self, events):
        """
        Handle events such as keyboard or mouse inputs.
        Args:
            events (list): A list of Pygame events to handle.
        """
        pass

    @abstractmethod
    def update(self):
        """
        Update the scene's state (e.g., game logic).
        """
        pass

    @abstractmethod
    def draw(self):
        """
        Draw the scene's visuals on the screen.
        """
        pass

    def run(self):
        """
        Main loop for the scene. Handles events, updates state, and draws visuals.
        """
        while self.running:
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()
            self.handle_events(events)

            # Update state
            self.update()

            # Draw visuals
            self.draw()

            # Refresh the display and control the frame rate
            pygame.display.flip()
            self.clock.tick(60)

    def stop(self):
        """
        Stop the scene and transition to another.
        """
        self.running = False
