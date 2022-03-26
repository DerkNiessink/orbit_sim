import pygame

from .settings import ViewSettings


def draw(window, settings: ViewSettings, screen_positions: list):
    """Draw the body relative to the body to track."""
    if settings.tail:
        for index in range(len(screen_positions)-1):

            pygame.draw.line(
                window,
                (100, 100, 100),
                start_pos=screen_positions[index],   
                end_pos =screen_positions[index+1],
                width=1,
                )


