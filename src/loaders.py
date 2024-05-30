import pygame

from os import walk
from os.path import join

from settings import GRAPHICS_DIR


def load_image(*path):
    """
    Loads an image file and converts it for optimal use with Pygame.

    :param str path: The file path to the image, relative to settings.GRAPHICS_DIR

    :returns: The loaded image as a Pygame Surface with per-pixel alpha.
    :rtype: pygame.Surface

    :raises pygame.error: If the image file could not be loaded.

    **Example:**

    .. code-block:: python

        image = load_image('path/to/image.png')
    """ # noqa 
    full_path = join(GRAPHICS_DIR, *path)
    image = pygame.image.load(full_path).convert_alpha()

    return image


def load_sprite_sheet(file, sprite_dimensions, positions=None):
    """
    This function loads a sprite sheet image and extracts individual sprites
    either sequentially or from specifc positions.

    Args
    ----

    file (str): The file path to the sprite sheet image.
    sprite_dimensions (tuple): sprite width and height in pixels.
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

    >>> all_sprites = load_sprite_sheet('path/to/image.png', (24, 24))

    Loading sprites from specific positions:

    >>> sprites = load_sprite_sheet('path/to/image.png',
                                    (24, 24),
                                    [(1,2), (1,3)])
    """
    full_path = join(GRAPHICS_DIR, file)
    sprite_sheet = pygame.image.load(full_path).convert_alpha()
    sheet_width, sheet_height = sprite_sheet.get_size()

    sprites = []

    if positions:
        for position in positions:
            rect = pygame.Rect(position[1] * sprite_dimensions[1],
                               position[0] * sprite_dimensions[0],
                               sprite_dimensions[0],
                               sprite_dimensions[1])
            sprite = sprite_sheet.subsurface(rect)
            sprites.append(sprite)
    else:
        for y in range(0, sheet_height, sprite_dimensions[1]):
            for x in range(0, sheet_width, sprite_dimensions[0]):
                rect = pygame.Rect(x, y,
                                   sprite_dimensions[0],
                                   sprite_dimensions[1])
                sprite = sprite_sheet.subsurface(rect)
                sprites.append(sprite)

    return sprites


def load_sprite_sheet_folder(path, sprite_dimensions):
    """
    Load every file in a folder and extracts individual sprites.

    Returns a dictionary composed by filenames without extensions as keys, and
    a list of extracted sprites as values.

    Given the following directory structure:

    enemy-1/
    ├── attack.png
    ├── idle.png
    └── walk.png

    Load the folder, extract all sprite sheets and print the images dict.

    >>> enemy_frames = load_sprite_sheet_folder('enemy-1', (24,24))
    >>> enemy_frames
    {
        "attack": [s1, s2, sN],
        "idle": [s1, s2, sN],
        "walk": [s1, s2, sN]
    }
    """
    sprites_dict = {}

    for folder_path, _, file_list in walk(join(GRAPHICS_DIR, path)):
        for filename in file_list:
            full_path = join(folder_path, filename)

            frames = load_sprite_sheet(full_path, sprite_dimensions)
            sprites_dict[filename.split('.')[0]] = frames

    return sprites_dict


def load_image_folder(*path):
    """
    Load every file in a folder as a image.

    Returns a dictionary composed by filenames without extensions as keys, and
    a list of extracted sprites as values.

    Given the following directory structure:

    tiles/
    ├── grass.png
    ├── water.png
    └── dirty.png

    Load the folder, extract all sprite sheets and print the images dict.

    >>> tile_images = load_image_folder('tiles')
    >>> tile_images
    {
        "grass": s1,
        "water": s1,
        "dirty": s1
    }
    """
    images_dict = {}

    for folder_path, _, file_list in walk(join(GRAPHICS_DIR, *path)):
        for filename in file_list:
            full_path = join(folder_path, filename)
            surface = pygame.image.load(full_path).convert_alpha()
            images_dict[filename.split('.')[0]] = surface

    return images_dict
