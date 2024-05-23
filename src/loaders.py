import pygame


def load_image(file):
    image = pygame.image.load(file).convert_alpha()

    return image


# images = load_sprite_sheet('../data/graphics/enemy-1.png', 24, 24)
# images = load_sprite_sheet('../data/graphics/tilemap-characters_packed.png', 24, 24, [(1,2), (1,3)])

def load_sprite_sheet(file, sprite_width, sprite_height, positions=None):
    sprite_sheet = pygame.image.load(file).convert_alpha()
    sheet_width, sheet_height = sprite_sheet.get_size()
    sprites = []

    if positions:
        for position in positions:
            rect = pygame.Rect(position[1] * sprite_height, position[0] * sprite_width, sprite_width, sprite_height)
            sprite = sprite_sheet.subsurface(rect)
            sprites.append(sprite)
    else:
        for y in range(0, sheet_height, sprite_height):
            for x in range(0, sheet_width, sprite_width):
                rect = pygame.Rect(x, y, sprite_width, sprite_height)
                sprite = sprite_sheet.subsurface(rect)
                sprites.append(sprite)

    return sprites
