import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()


class Tile(Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)
