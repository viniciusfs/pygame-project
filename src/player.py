import pygame

from settings import vector


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_group, frames):
        super().__init__(groups)

        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-10, 0)
        self.old_rect = self.hitbox_rect.copy()

        self.direction = vector()
        self.speed = 150
        self.animation_speed = 5
        self.gravity = 1200

        self.facing_left = True

        self.jumping = False
        self.jump_height = 400

        self.collision_group = collision_group
        self.on_surface = False

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

        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_SPACE]:
            self.jumping = True

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        self.direction.y += self.gravity / 2 * dt
        self.hitbox_rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')

        if self.jumping:
            if self.on_surface:
                self.direction.y = -self.jump_height

            self.jumping = False

        self.rect.center = self.hitbox_rect.center

    def check_on_surface(self):
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        collide_rects = [sprite.rect for sprite in self.collision_group]
        self.on_surface = True if floor_rect.collidelist(collide_rects) >= 0 else False

    def collision(self, axis):
        for sprite in self.collision_group:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal':
                    # left
                    if (self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right)):
                        self.hitbox_rect.left = sprite.rect.right
                    # right
                    if (self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left)):
                        self.hitbox_rect.right = sprite.rect.left
                elif axis == 'vertical':
                    # top
                    if (self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom)):
                        self.hitbox_rect.top = sprite.rect.bottom
                    # bottom
                    if (self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top)):
                        self.hitbox_rect.bottom = sprite.rect.top

                    self.direction.y = 0

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = self.image if self.facing_left else pygame.transform.flip(self.image, True, False)
