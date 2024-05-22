import pygame
from pytmx.util_pygame import load_pygame

from settings import WHITE, BLACK, GAME_WIDTH, GAME_HEIGHT, TILE_WIDTH, TILE_HEIGHT
from sprites import Sprite, Tile


class Controller:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.exit = False

    def add_state(self, name, state):
        self.states[name] = state

    def change_state(self, name):
        if self.current_state:
            self.current_state.exit()

        self.current_state = self.states[name]
        self.current_state.enter()

    def update(self, events):
        if self.current_state:
            self.current_state.update(events)

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)


class GameState:
    def __init__(self, controller):
        self.controller = controller

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, events):
        pass

    def draw(self, screen):
        pass


class SplashScreen(GameState):
    def __init__(self, controller):
        super().__init__(controller)
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render('Splash Screen', True, WHITE)
        self.text_rect = self.text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2))

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.controller.change_state('PlataformerGame')

    def draw(self, screen):
        screen.fill(BLACK)
        screen.blit(self.text, self.text_rect)


class ExitScreen(GameState):
    def __init__(self, controller):
        super().__init__(controller)
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render('Exit Screen', True, BLACK)
        self.text_rect = self.text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2))

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.controller.exit = True

    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(self.text, self.text_rect)


class PlatformerGame(GameState):
    def __init__(self, controller):
        super().__init__(controller)

        self.sprite_groups = {
            'tiles': pygame.sprite.Group(),
            'objects': pygame.sprite.Group()
        }

        tmx_data = load_pygame('../misc/tiled/example_levels/testing-1.tmx')

        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surface in layer.tiles():
                    pos = (x * TILE_WIDTH, y * TILE_HEIGHT)
                    Tile(pos=pos, surface=surface,
                         groups=self.sprite_groups['tiles'])

        for obj in tmx_data.objects:
            pos = obj.x, obj.y
            if obj.image:
                Sprite(pos=pos, surface=obj.image,
                       groups=self.sprite_groups['objects'])

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.controller.change_state('ExitScreen')

    def draw(self, screen):
        screen.fill("skyblue")
        self.sprite_groups['tiles'].draw(screen)
        self.sprite_groups['objects'].draw(screen)
