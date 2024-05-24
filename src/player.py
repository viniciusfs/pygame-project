import pygame

from settings import vector


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_group):
        super().__init__(groups)
        self.image = pygame.Surface((16, 18))
        self.image.fill('red')
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        self.direction = vector()
        self.speed = 200
        self.gravity = 400
        self.jumping = False
        self.jump_height = 200

        self.collision_group = collision_group
        self.on_surface = False


    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)

        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1

        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_SPACE]:
            self.jumping = True

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')

        if self.jumping:
            if self.on_surface:
                self.direction.y = -self.jump_height

            self.jumping = False

    def check_on_surface(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        collide_rects = [sprite.rect for sprite in self.collision_group]
        self.on_surface = True if floor_rect.collidelist(collide_rects) >= 0 else False

    def collision(self, axis):
        for sprite in self.collision_group:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # left
                    if (self.rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right)):
                        self.rect.left = sprite.rect.right
                    # right
                    if (self.rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left)):
                        self.rect.right = sprite.rect.left
                elif axis == 'vertical':
                    # top
                    if (self.rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom)):
                        self.rect.top = sprite.rect.bottom
                    # bottom
                    if (self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top)):
                        self.rect.bottom = sprite.rect.top

                    self.direction.y = 0

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
        self.check_on_surface()
