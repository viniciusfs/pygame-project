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

        self.collision_group = collision_group

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)

        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1

        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')

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

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
