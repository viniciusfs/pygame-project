import pygame

from pygame.math import Vector2 as vector


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_group, frames, particle_emitter):
        super().__init__(groups)

        self.state = 'idle'
        self.last_state = self.state

        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.state][self.frame_index]

        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-10, -3)
        self.hitbox_rect.midbottom = self.rect.midbottom
        self.old_rect = self.hitbox_rect.copy()

        self.direction = vector()
        self.speed = 150
        self.animation_speed = 5
        self.gravity = 1200

        self.facing_left = True

        self.jump_key = False
        self.jump_height = 400

        self.collision_group = collision_group
        self.on_surface = False

        self.dust_effect = particle_emitter

    def update(self, dt):
        self.old_rect = self.hitbox_rect.copy()
        self.input()
        self.move(dt)
        self.check_on_surface()
        self.animate(dt)

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)

        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
            self.facing_left = False

        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
            self.facing_left = True

        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x  # noqa: E501

        if keys[pygame.K_SPACE]:
            self.jump_key = True

    def move(self, dt):
        # horizontal move
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # vertical move
        if self.jump_key:
            if self.on_surface:
                self.direction.y = -self.jump_height
                self.dust_effect.emit(
                    count=2,
                    pos=self.hitbox_rect.midbottom,
                    dispersion_width=self.rect.width
                )
            self.jump_key = False

        self.direction.y += self.gravity / 2 * dt
        self.hitbox_rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')

        self.rect.midbottom = self.hitbox_rect.midbottom

        if (self.on_surface and self.last_state == 'falling'):
            self.dust_effect.emit(
                count=5,
                pos=self.hitbox_rect.midbottom,
                dispersion_width=self.rect.width
            )

        if (self.on_surface and (self.direction.x == 0) and
                (self.direction.y == 0)):
            self.state = 'idle'

        if (self.on_surface and (self.direction.x != 0) and
                (self.direction.y == 0)):
            self.state = 'walking'

        if not self.on_surface and (self.direction.y > 0):
            self.state = 'falling'

        if not self.on_surface and (self.direction.y < 0):
            self.state = 'jumping'

    def check_on_surface(self):
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft,
                                 (self.hitbox_rect.width, 2))
        collide_rects = [sprite.rect for sprite in self.collision_group]
        self.last_state = self.state
        self.on_surface = True if floor_rect.collidelist(collide_rects) >= 0 else False  # noqa: E501

    def collision(self, axis):
        for sprite in self.collision_group:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal':
                    # left
                    if (self.hitbox_rect.left <= sprite.rect.right and
                            int(self.old_rect.left) >= int(sprite.old_rect.right)):  # noqa: E501
                        self.hitbox_rect.left = sprite.rect.right
                    # right
                    if (self.hitbox_rect.right >= sprite.rect.left and
                            int(self.old_rect.right) <= int(sprite.old_rect.left)):  # noqa: E501
                        self.hitbox_rect.right = sprite.rect.left
                elif axis == 'vertical':
                    # top
                    if (self.hitbox_rect.top <= sprite.rect.bottom and
                            int(self.old_rect.top) >= int(sprite.old_rect.bottom)):  # noqa: E501
                        self.hitbox_rect.top = sprite.rect.bottom
                    # bottom
                    if (self.hitbox_rect.bottom >= sprite.rect.top and
                            int(self.old_rect.bottom) <= int(sprite.old_rect.top)):  # noqa: E501
                        self.hitbox_rect.bottom = sprite.rect.top

                    self.direction.y = 0

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[self.state][int(self.frame_index %
                                                 len(self.frames[self.state]))]
        self.image = self.image if self.facing_left else pygame.transform.flip(self.image, True, False)  # noqa: E501
