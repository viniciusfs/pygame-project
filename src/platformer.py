import pygame
from pytmx.util_pygame import load_pygame
from os.path import join

from settings import TILE_SIZE, TILED_DIR
from states import GameState
from sprites import Sprite, Tile, AnimatedSprite
from player import Player
from loaders import load_sprite_sheet


class PlatformerGame(GameState):
    def __init__(self, controller):
        super().__init__(controller)

        self.player = None
        self.assets = {}
        self.sprite_groups = {
            'all': pygame.sprite.Group(),
            'items': pygame.sprite.Group(),
            'coins': pygame.sprite.Group(),
            'terrain': pygame.sprite.Group()
        }

        self.levels = {
            1: 'example_levels/testing-1.tmx',
            2: 'example_levels/testing-2.tmx',
            3: 'example_levels/testing-3.tmx'
        }
        self.current_level = 1

        self.stats = {'coins': 0, 'score': 0}

    def enter(self):
        self.load_assets()
        self.load_map(self.levels[self.current_level], self.sprite_groups)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.controller.change_state('ExitScreen')

        self.sprite_groups['all'].update(dt)
        self.item_collision()

    def draw(self, screen):
        screen.fill("skyblue")
        self.sprite_groups['all'].draw(screen)

    def change_level(self):
        for group in self.sprite_groups.values():
            group.empty()

        self.current_level += 1
        if self.current_level > len(self.levels):
            self.current_level = 1

        self.load_map(self.levels[self.current_level], self.sprite_groups)

    def load_assets(self):
        self.assets['player'] = load_sprite_sheet(
            'tilemap-characters_packed.png',
            (24, 24),
            [(0, 0), (0, 1)]
        )

        self.assets['coin'] = load_sprite_sheet(
            'tilemap_packed.png',
            (18, 18),
            [(7, 11), (7, 12)]
        )

    def load_map(self, filename, sprite_groups):
        tmx_data = load_pygame(join(TILED_DIR, filename))

        # terrain tiles
        for x, y, surface in tmx_data.get_layer_by_name('terrain').tiles():
            Tile(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surface=surface,
                groups=(sprite_groups['terrain'], sprite_groups['all'])
            )

        # background tiles
        for x, y, surface in tmx_data.get_layer_by_name('background').tiles():
            Tile(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surface=surface,
                groups=(sprite_groups['all'])
            )

        # foreground tiles
        for x, y, surface in tmx_data.get_layer_by_name('foreground').tiles():
            Tile(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surface=surface,
                groups=(sprite_groups['all'])
            )

        # items objects
        for obj in tmx_data.get_layer_by_name('items'):
            if obj.name == 'checkpoint':
                self.checkpoint_rect = pygame.Rect(obj.x,
                                                   obj.y,
                                                   obj.width,
                                                   obj.height)

            if obj.image:
                if obj.name == 'coin':
                    AnimatedSprite(
                        pos=(obj.x, obj.y),
                        groups=(sprite_groups['coins'], sprite_groups['all']),
                        hitbox_offset=(-6, -6),
                        frames=self.assets['coin'],
                        animation_speed=5
                    )
                else:
                    Sprite(
                        pos=(obj.x, obj.y),
                        surface=obj.image,
                        groups=(sprite_groups['items'], sprite_groups['all'])
                    )

        # player
        for obj in tmx_data.get_layer_by_name('player'):
            if obj.name == 'player':
                self.player = Player(pos=(obj.x, obj.y),
                                     groups=sprite_groups['all'],
                                     collision_group=sprite_groups['terrain'],
                                     frames=self.assets['player'])

    def item_collision(self):
        collision = pygame.sprite.spritecollide(self.player,
                                                self.sprite_groups['items'],
                                                True)
        if collision:
            self.stats['score'] += 100

            print("Player captured a key. {'coins': %d, 'score': %d}" % (
                self.stats['coins'], self.stats['score'])
            )

        for coin in self.sprite_groups['coins']:
            if coin.hitbox_rect.colliderect(self.player.hitbox_rect):
                self.stats['coins'] += 1
                self.stats['score'] += 10

                print("Player captured a coin. {'coins': %d, 'score': %d}" % (
                    self.stats['coins'], self.stats['score'])
                )
                coin.kill()

        if pygame.Rect.colliderect(self.checkpoint_rect,
                                   self.player.hitbox_rect):
            print("Player reached a checkpoint!")
            self.change_level()
