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


class Collidable(Sprite):
    def __init__(self, pos, surface, groups, hitbox_offset):
        super().__init__(pos, surface, groups)

        self.hitbox_rect = self.rect.inflate(hitbox_offset[0],
                                             hitbox_offset[1])
        self.old_rect = self.hitbox_rect.copy()


class AnimatedSprite(Collidable):
    def __init__(self, pos, groups, hitbox_offset, frames, animation_speed):
        self.frames = frames
        self.frame_index = 0

        super().__init__(pos=pos,
                         surface=self.frames[self.frame_index],
                         groups=groups,
                         hitbox_offset=hitbox_offset)

        self.animation_speed = animation_speed

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)
