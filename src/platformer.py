import pygame
from pytmx.util_pygame import load_pygame
from os.path import join

from settings import TILE_SIZE, TILED_DIR
from states import GameState
from sprites import Sprite, Tile
from player import Player


class PlatformerGame(GameState):
    def __init__(self, controller):
        super().__init__(controller)

        self.sprite_groups = {
            'all': pygame.sprite.Group(),
            'items': pygame.sprite.Group(),
            'collision': pygame.sprite.Group()
        }

    def enter(self):
        self.load_map('example_levels/testing-1.tmx', self.sprite_groups)

    def load_map(self, filename, sprite_groups):
        tmx_data = load_pygame(join(TILED_DIR, filename))

        # terrain tiles
        for x, y, surface in tmx_data.get_layer_by_name('terrain').tiles():
            Tile(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surface=surface,
                groups=(sprite_groups['collision'], sprite_groups['all'])
            )

        # background tiles
        for x, y, surface in tmx_data.get_layer_by_name('background').tiles():
            Tile(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surface=surface,
                groups=(sprite_groups['all'])
            )

        # foreground tiles
        for x, y, surface in tmx_data.get_layer_by_name('foreground').tiles():
            Tile(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surface=surface,
                groups=(sprite_groups['all'])
            )

        # items objects
        for obj in tmx_data.get_layer_by_name('items'):
            if obj.image:
                Sprite(
                    pos=(obj.x, obj.y),
                    surface=obj.image,
                    groups=(sprite_groups['items'], sprite_groups['all'])
                )

        # player
        for obj in tmx_data.get_layer_by_name('player'):
            if obj.name == 'player':
                self.player = Player(pos=(obj.x, obj.y),
                                     groups=sprite_groups['all'],
                                     collision_group=sprite_groups['collision'])

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.controller.change_state('ExitScreen')

        self.sprite_groups['all'].update(dt)

    def draw(self, screen):
        screen.fill("skyblue")
        self.sprite_groups['all'].draw(screen)
