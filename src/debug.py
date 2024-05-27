import pygame

from settings import WHITE, BLACK


def debug(message, pos, surface, font):
    debug_message = font.render(str(message), True, WHITE)
    debug_rect = debug_message.get_rect(topleft=pos)
    pygame.draw.rect(surface, BLACK, debug_rect)
    surface.blit(debug_message, debug_rect)
