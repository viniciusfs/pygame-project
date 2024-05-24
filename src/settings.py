import os

from pygame.math import Vector2 as vector


GAME_WIDTH = 468
GAME_HEIGHT = 270
SCREEN_WIDTH = GAME_WIDTH * 2
SCREEN_HEIGHT = GAME_HEIGHT * 2

TILE_SIZE = 18
TILES_X = 26
TILES_Y = 15

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
GRAPHICS_DIR = os.path.join(ROOT_DIR, 'data/graphics')
TILED_DIR = os.path.join(ROOT_DIR, 'misc/tiled')
