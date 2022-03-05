import collections
import math

import pygame
import numpy as np


def distance(point1: tuple[float], point2: tuple[float]) -> float:
    """Return the distance between point 1 and 2."""
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def zoom(coordinates, scale_factor, zoom_level):
    return [(x * scale_factor * zoom_level, y * scale_factor * zoom_level) for x, y in coordinates]


def pan(coordinates, origin):
    return [(x + origin_x, y + origin_y) for (x, y), (origin_x, origin_y) in zip(coordinates, origin)]


class PhysicalObjectView:

    DEQUE_MAXLEN = 7000

    def __init__(self, name, scale_factor, colour, image, body):
        self.name = name
        self.scale_factor = scale_factor
        self.body_model = body
        self.colour = colour
        self.originalImage = pygame.image.load(image)
        self.positions = collections.deque(maxlen=self.DEQUE_MAXLEN)

    def radius(self, zoom_level):
        return max(self.body_model.radius * self.scale_factor * zoom_level, 3 * math.log(zoom_level))

    def draw(self, window, zoomLevel, offset, bodyToTrack):
        """Draw the body relative to the body to track."""
        self.positions.append((self.body_model.x, self.body_model.y))
        positions = [(0, 0) for _ in self.positions] if self == bodyToTrack else pan(self.positions, bodyToTrack.positions)
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
            pygame.transform.scale(self.originalImage, (self.radius(zoomLevel) * 2, self.radius(zoomLevel) * 2)),
            (self.x_to_draw - self.radius(zoomLevel), self.y_to_draw - self.radius(zoomLevel)),
        )

    def get_distance_pixels(self, x: float, y: float) -> float:
        """Get the distance in pixels to the given coordinate"""
        return distance((self.x_to_draw, self.y_to_draw), (x, y))
