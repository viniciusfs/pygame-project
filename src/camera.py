import pygame

from settings import GAME_WIDTH, GAME_HEIGHT


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.offset = pygame.math.Vector2()
        self.camera_borders = {'left': 150, 'right': 150, 'top': 0, 'bottom': 0}

        self.camera_rect = pygame.Rect(
            self.camera_borders['left'],
            self.camera_borders['top'],
            GAME_WIDTH - (self.camera_borders['left'] + self.camera_borders['right']),
            GAME_HEIGHT - (self.camera_borders['top'] + self.camera_borders['bottom'])
        )

    def update_target(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left

        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def custom_draw(self, screen, target):
        self.update_target(target)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)
