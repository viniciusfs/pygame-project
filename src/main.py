import sys
import pygame
from pytmx.util_pygame import load_pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_WIDTH, TILE_HEIGHT
from sprites import Sprite, Tile


class Game():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.sprite_groups = {
            'tiles': pygame.sprite.Group(),
            'objects': pygame.sprite.Group()
        }

    def run(self):
        while True:
            self.load_level(self.sprite_groups)
            self.get_events()
            self.render()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def render(self):
        self.screen.fill("skyblue")
        self.sprite_groups['tiles'].draw(self.screen)
        self.sprite_groups['objects'].draw(self.screen)

        pygame.display.update()

    def load_level(self, sprite_groups):
        tmx_data = load_pygame('../misc/tiled/example_levels/testing-1.tmx')

        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surface in layer.tiles():
                    pos = (x * TILE_WIDTH, y * TILE_HEIGHT)
                    Tile(pos=pos, surface=surface,
                         groups=sprite_groups['tiles'])

        for obj in tmx_data.objects:
            pos = obj.x, obj.y
            if obj.image:
                Sprite(pos=pos, surface=obj.image,
                       groups=sprite_groups['objects'])


if __name__ == '__main__':
    game = Game()
    game.run()
