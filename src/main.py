import sys
import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_WIDTH, GAME_HEIGHT
from states import Controller, SplashScreen, ExitScreen
from platformer import PlatformerGame
from particles import TestParticles


class Game():
    """
    Main game class that initializes and runs the game loop.

    Attributes:
        screen: The main display surface.
        canvas: The surface where the game is drawn before scaling to the screen.
        clock: The game clock for controlling the frame rate.
        running: A flag to indicate if the game is running or not.
        controller: The game state controller managing the different game states.
    """ # noqa
    def __init__(self):
        """
        Initializes the game, sets up the display and prepare the game states.
        """
        pygame.init()
        pygame.display.set_caption("The Mini Games Project")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.clock = pygame.time.Clock()

        self.controller = Controller()
        self.controller.add_state('SplashScreen',
                                  SplashScreen(controller=self.controller))
        self.controller.add_state('ExitScreen',
                                  ExitScreen(controller=self.controller))
        self.controller.add_state('PlatformerGame',
                                  PlatformerGame(controller=self.controller))
        self.controller.add_state('TestParticles',
                                  TestParticles(controller=self.controller))

        self.controller.change_state('TestParticles')
        self.running = True

    def run(self):
        """
        Starts the game loop, get events, update current state and render
        the game window.
        """
        while self.running:
            dt = self.clock.tick() / 1000

            if self.controller.exit:
                self.running = False
                continue

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    continue

            self.controller.update(dt, events)
            self.controller.draw(self.canvas)

            self.screen.blit(
                pygame.transform.scale(self.canvas, (SCREEN_WIDTH,
                                                     SCREEN_HEIGHT)),
                (0, 0)
            )
            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
