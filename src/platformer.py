import pygame
from pytmx.util_pygame import load_pygame

from settings import TILE_SIZE
from states import GameState
from sprites import Sprite, Tile


class PlatformerGame(GameState):
    def __init__(self, controller):
        super().__init__(controller)

        self.sprite_groups = {
            'tiles': pygame.sprite.Group(),
            'objects': pygame.sprite.Group()
        }

        tmx_data = load_pygame('../misc/tiled/example_levels/testing-1.tmx')

        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surface in layer.tiles():
                    pos = (x * TILE_SIZE, y * TILE_SIZE)
                    Tile(pos=pos, surface=surface,
                         groups=self.sprite_groups['tiles'])

        for obj in tmx_data.objects:
            pos = obj.x, obj.y
            if obj.image:
                Sprite(pos=pos, surface=obj.image,
                       groups=self.sprite_groups['objects'])

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.controller.change_state('ExitScreen')

    def draw(self, screen):
        screen.fill("skyblue")
        self.sprite_groups['tiles'].draw(screen)
        self.sprite_groups['objects'].draw(screen)
