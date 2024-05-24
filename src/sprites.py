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


class AnimatedSprite(Sprite):
    def __init__(self, pos, surface, groups, frames, animation_speed):
        self.frames = frames
        self.frame_index = 0

        super().__init__(pos=pos,
                         surface=self.frames[self.frame_index],
                         groups=groups)

        self.animation_speed = animation_speed

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)
