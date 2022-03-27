import collections

import pygame
from pygame.math import Vector2

from .settings import ViewSettings


class DrawTail:
    def __init__(self):
        self.drawables = []

    def make_drawable(self, screen_positions, colours):
        self.drawables = []
        for (body_screen_positions, colour) in zip(screen_positions, colours):
            for index in range(len(body_screen_positions)-1):
                self.drawables.append((body_screen_positions[index], body_screen_positions[index + 1], colour))

        self.drawables = sorted(self.drawables, key=lambda tup: tup[0].z)     

    def draw(self, window, settings: ViewSettings, screen_positions: collections.deque[list[Vector2]], colours: list):
        if settings.tail:
            self.make_drawable(screen_positions, colours)
            for line_segment in self.drawables:
                pygame.draw.line(
                    window,
                    line_segment[2],
                    start_pos=Vector2(line_segment[0].x, line_segment[0].y),
                    end_pos=Vector2(line_segment[1].x, line_segment[1].y),   
                    width=5,
                        )


