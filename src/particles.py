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
                 fading=False,
                 fade_speed=200,
                 shrinking=False,
                 shrink_speed=0):
        super().__init__()
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed
        self.size = size
        self.lifespan = lifespan
        self.fading = fading
        self.fade_speed = fade_speed
        self.shrinking = shrinking
        self.shrink_speed = shrink_speed
        self.creation_time = pygame.time.get_ticks()

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


class DustEffect(ParticleGroup):
    def __init__(self):
        super().__init__(particle_class=GravityParticle)

    def randomize_particle_attributes(self):
        colors = ["gray", "gray100", "gray60"]

        attr_dict = {
            'size': random.randint(2, 6),
            'speed': random.randint(25, 50),
            'color': random.choice(colors),
            'lifespan': random.randint(500, 1000),
            'fade_speed': 500
        }

        return attr_dict

    def emit(self, count, pos, dispersion_width):
        center = dispersion_width / 2
        leftmost = int(pos[0] - (center / 2))
        rightmost = int(pos[0] + (center / 2))

        for _ in range(count):
            particle_x = random.randint(leftmost, rightmost)

            if particle_x < center:
                directions = [
                    pygame.math.Vector2(0.10, -1),
                    pygame.math.Vector2(0.25, -0.75),
                    pygame.math.Vector2(0.35, -0.50)
                ]
            else:
                directions = [
                    pygame.math.Vector2(-0.10, -1),
                    pygame.math.Vector2(-0.25, -0.75),
                    pygame.math.Vector2(-0.35, -0.50),
                ]

            particle_direction = random.choice(directions)
            particle_position = particle_x, pos[1]
            particle_attrs = self.randomize_particle_attributes()

            particle = self.particle_class(
                pos=particle_position,
                direction=particle_direction,
                gravity=3,
                fading=True,
                **particle_attrs
            )
            self.add(particle)


class TestParticles(GameState):
    def __init__(self, controller):
        super().__init__(controller)

        self.particle_group = DustEffect()

    def update(self, dt, events):
        count = random.randint(5, 15)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                raw_position = pygame.mouse.get_pos()
                downscaled_x = raw_position[0] / 2
                downscaled_y = raw_position[1] / 2
                position = downscaled_x, downscaled_y

                self.particle_group.emit(
                    count=count,
                    pos=position,
                    dispersion_width=24
                )

        self.particle_group.update(dt)

    def draw(self, screen):
        screen.fill('black')
        self.particle_group.draw(screen)
