import pygame
import random

from settings import GAME_WIDTH, GAME_HEIGHT
from states import GameState


class Particle(pygame.sprite.Sprite):
    def __init__(self,
                 pos,
                 color,
                 direction,
                 speed,
                 size,
                 lifespan,
                 fade=False,
                 shrink=False):
        super().__init__()
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed
        self.size = size
        self.lifespan = lifespan
        self.fading = fade
        self.shrinking = shrink

        self.creation_time = pygame.time.get_ticks()
        self.fade_speed = 200
        self.alpha = 255

        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")

        pygame.draw.circle(surface=self.image, color=self.color,
                           center=(self.size/2, self.size/2),
                           radius=self.size/2)

        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        self.check_lifespan()
        self.move(dt)
        self.check_position()

        if self.fading:
            self.fade(dt)

        if self.shrinking:
            self.shrink()

    def check_lifespan(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time > self.lifespan:
            self.kill()

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def check_position(self):
        if (self.pos[0] < -50 or self.pos[0] > GAME_WIDTH + 50 or self.pos[1] < -50 or self.pos[1] > GAME_HEIGHT + 50):  # noqa: E501
            self.kill()

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)

        if self.alpha <= 0:
            self.kill()

    def shrink(self):
        pass


class ParticleGroup(pygame.sprite.Group):
    def __init__(self, particle_class=Particle):
        super().__init__()
        self.particle_class = particle_class

    def update(self, dt):
        super().update(dt)

    def emit(self, count, pos, color, direction, speed, size, lifespan, **kwargs):  # noqa: E501
        for _ in range(count):
            particle = self.particle_class(
                pos=pos,
                color=color,
                direction=direction,
                speed=speed,
                size=size,
                lifespan=lifespan,
                **kwargs
            )
            self.add(particle)


class GravityParticle(Particle):
    def __init__(self, gravity, **kargs):
        super().__init__(**kargs)
        self.gravity = gravity

    def move(self, dt):
        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt

        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos


class TestParticles(GameState):
    def __init__(self, controller):
        super().__init__(controller)

        self.particle_group = ParticleGroup(particle_class=GravityParticle)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                raw_position = pygame.mouse.get_pos()
                downscaled_x = raw_position[0] / 2
                downscaled_y = raw_position[1] / 2
                pos = downscaled_x + random.randint(-10, 10), downscaled_y + random.randint(-10, 10)  # noqa: E501
                color = "gray"
                speed = random.randint(50, 100)
                size = random.randint(3, 10)

                if event.button == 1:
                    direction = pygame.math.Vector2(0.5, -0.5)
                if event.button == 3:
                    direction = pygame.math.Vector2(-0.5, -0.5)

                self.particle_group.emit(
                    count=1,
                    gravity=2.5,
                    pos=pos,
                    color=color,
                    direction=direction,
                    speed=speed,
                    size=size,
                    lifespan=2000,
                    fade=True
                )

        self.particle_group.update(dt)

    def draw(self, screen):
        screen.fill('black')
        self.particle_group.draw(screen)
