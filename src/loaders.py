import pygame


def load_image(file):
    """
    Loads an image file and converts it for optimal use with Pygame.

    :param str file: The file path to the image.

    :returns: The loaded image as a Pygame Surface with per-pixel alpha.
    :rtype: pygame.Surface

    :raises pygame.error: If the image file could not be loaded.

    **Example:**

    .. code-block:: python

        image = load_image('path/to/image.png')
    """
    image = pygame.image.load(file).convert_alpha()

    return image


def load_sprite_sheet(file, sprite_width, sprite_height, positions=None):
    """
    This function loads a sprite sheet image and extracts individual sprites
    either sequentially or from specifc positions.

    Args
    ----

    file (str): The file path to the sprite sheet image.
    sprite_width (int): The width of each sprite in the sheet.
    sprite_height (int): The height of each sprite in the sheet.
    positions (list of tuple, optional): A list of (row, column) tuples
                                         specifying the positions of sprites to
                                         extract. If None, all sprites are
                                         extracted sequentially.

    Returns
    -------

    list of pygame.Surface: A list of surfaces, each representing an extracted
                            sprite.

    Examples
    --------

    Loading all sprites sequentially:

    >>> all_sprites = load_sprite_sheet('path/to/image.png', 24, 24)

    Loading sprites from specific positions:

    >>> sprites = load_sprite_sheet('path/to/image.png', 24, 24, [(1,2), (1,3)])
    """
    sprite_sheet = pygame.image.load(file).convert_alpha()
    sheet_width, sheet_height = sprite_sheet.get_size()

    sprites = []

    if positions:
        for position in positions:
            rect = pygame.Rect(position[1] * sprite_height,
                               position[0] * sprite_width,
                               sprite_width,
                               sprite_height)
            sprite = sprite_sheet.subsurface(rect)
            sprites.append(sprite)
    else:
        for y in range(0, sheet_height, sprite_height):
            for x in range(0, sheet_width, sprite_width):
                rect = pygame.Rect(x, y, sprite_width, sprite_height)
                sprite = sprite_sheet.subsurface(rect)
                sprites.append(sprite)

    return sprites
