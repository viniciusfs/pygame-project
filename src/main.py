import sys
import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_WIDTH, GAME_HEIGHT
from states import Controller, SplashScreen, ExitScreen, PlatformerGame


class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The Mini Games Project")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True

        self.controller = Controller()
        self.controller.add_state('SplashScreen',
                                  SplashScreen(controller=self.controller))
        self.controller.add_state('ExitScreen',
                                  ExitScreen(controller=self.controller))
        self.controller.add_state('PlataformerGame',
                                  PlatformerGame(controller=self.controller))

        self.controller.change_state('SplashScreen')

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.controller.update(events)
            self.controller.draw(self.canvas)

            if self.controller.exit:
                self.running = False

            self.screen.blit(
                pygame.transform.scale(self.canvas, (SCREEN_WIDTH, SCREEN_HEIGHT)),
                (0, 0)
            )
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
