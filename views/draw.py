import collections

import pygame
from pygame.math import Vector2

from .settings import ViewSettings


class DrawTail:
    def __init__(self):
        self.drawables = []

    def make_drawable(self, screen_positions, z_coordinates, colours):
        self.drawables = []
        for (body_screen_positions, body_z_coordinates, colours) in zip(screen_positions, z_coordinates, colours):
            for index in range(len(body_screen_positions)-1):
                self.drawables.append((body_screen_positions[index], body_screen_positions[index + 1], body_z_coordinates[index], colours[2]))

        self.drawables.sort(key=lambda tup: tup[2])        

    def draw(self, window, settings: ViewSettings, screen_positions: collections.deque[list[Vector2]], z_coordinates: collections.deque[list[float]], colours: list):
        if settings.tail:
            self.make_drawable(screen_positions, z_coordinates, colours)
            for line_segment in self.drawables:
                pygame.draw.line(
                    window,
                    line_segment[3],
                    start_pos=line_segment[0],
                    end_pos= line_segment[1],   
                    width=1,
                        )


