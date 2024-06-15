import os
import pygame


TILE_SIZE = 18
TILES_X = 26
TILES_Y = 15
GAME_WIDTH = TILES_X * TILE_SIZE    # 468
GAME_HEIGHT = TILES_Y * TILE_SIZE   # 270
SCREEN_WIDTH = GAME_WIDTH * 2
SCREEN_HEIGHT = GAME_HEIGHT * 2

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
GRAPHICS_DIR = os.path.join(ROOT_DIR, 'data/graphics')
TILED_DIR = os.path.join(ROOT_DIR, 'data/tiled')
FONTS_DIR = os.path.join(ROOT_DIR, 'data/fonts')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.font.init()
DEBUG_FONT = pygame.font.Font(os.path.join(FONTS_DIR, 'grand9k-pixel.ttf'), 8)
