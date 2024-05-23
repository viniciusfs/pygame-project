import pygame

from settings import WHITE, BLACK, GAME_WIDTH, GAME_HEIGHT


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
