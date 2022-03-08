import collections
import math
from random import randrange
from typing import cast

import pygame
import numpy as np


def distance(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    """Return the distance between point 1 and 2."""
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def zoom(coordinates, scale_factor, zoom_level):
    return [
        (x * scale_factor * zoom_level, y * scale_factor * zoom_level)
        for x, y in coordinates
    ]


def relative_coordinates(coordinates, origin):
    """Transform the coordinates into coordinates relative to the origin."""
    return [
        (x - origin_x, y - origin_y)
        for (x, y), (origin_x, origin_y) in zip(coordinates, origin)
    ]


def pan(coordinates, offsets):
    """Pan the coordinates with the given offsets."""
    return [
        (x + origin_x, y + origin_y)
        for (x, y), (origin_x, origin_y) in zip(coordinates, offsets)
    ]


def average_colour(image: pygame.Surface) -> tuple[int, int, int]:
    """Calculate the average colour of an image by sampling a limited number of pixels."""
    width, height = image.get_width(), image.get_height()
    sample_size = round(math.sqrt(width * height))
    random_points = [
        (randrange(0, width), randrange(0, height)) for _ in range(sample_size)
    ]
    colours = [cast(pygame.Color, image.get_at(point)) for point in random_points]
    colours = [
        colour for colour in colours if colour.a > 0
    ]  # Ignore transparent pixels
    average_r = round(sum(colour.r for colour in colours) / len(colours))
    average_g = round(sum(colour.g for colour in colours) / len(colours))
    average_b = round(sum(colour.b for colour in colours) / len(colours))
    return (average_r, average_g, average_b)


class PhysicalObjectView:

    DEQUE_MAXLEN = 7000

    def __init__(self, name, scale_factor, colour, image, body):
        self.name = name
        self.scale_factor = scale_factor
        self.body_model = body
        self.originalImage = pygame.image.load(image)
        self.colour = colour or average_colour(self.originalImage)
        self.positions = collections.deque(maxlen=self.DEQUE_MAXLEN)

    def radius(self, zoom_level):
        if self.name == "Center of mass":
            return 10
        else:
            return max(
                self.body_model.radius * self.scale_factor * zoom_level,
                3 * math.log(zoom_level),
            )

    def draw(self, window, zoomLevel, offset, bodyToTrack):
        """Draw the body relative to the body to track."""
        self.positions.append((self.body_model.x, self.body_model.y))
        positions = relative_coordinates(self.positions, bodyToTrack.positions)
        positions = zoom(positions, self.scale_factor, zoomLevel)
        positions = pan(positions, [(offset[0], offset[1]) for _ in positions])
        self.x_to_draw, self.y_to_draw = positions[-1]
        if self != bodyToTrack and len(positions) > 2:
            pygame.draw.lines(
                window,
                self.colour,
                closed=False,
                points=np.array(positions),
                width=1,
            )
        window.blit(
            pygame.transform.scale(
                self.originalImage,
                (self.radius(zoomLevel) * 2, self.radius(zoomLevel) * 2),
            ),
            (
                self.x_to_draw - self.radius(zoomLevel),
                self.y_to_draw - self.radius(zoomLevel),
            ),
        )

    def draw_label(self, window, zoomLevel):
        """Draw a label of the name of the body"""

        min_size = 15
        # formula for size of label based on zoomlevel
        size = int(1 / zoomLevel ** 0.05)

        if size < min_size:
            size = min_size

        font = pygame.font.SysFont("monospace", size)
        label_zoom = font.render(
            f"{self.name}",
            1,
            (255, 255, 255),
        )
        window.blit(
            label_zoom,
            (
                self.x_to_draw + self.radius(zoomLevel),
                self.y_to_draw + self.radius(zoomLevel),
            ),
        )

    def get_distance_pixels(self, x: float, y: float) -> float:
        """Get the distance in pixels to the given coordinate"""
        return distance((self.x_to_draw, self.y_to_draw), (x, y))
