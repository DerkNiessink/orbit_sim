import collections
import math
from random import randrange
from typing import cast

import pygame


def distance(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    """Return the distance between point 1 and 2."""
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


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


def pan(coordinates, offset):
    """Pan the coordinates with the given offset."""
    return [
        (x + offset[0], y + offset[1]) for (x, y) in coordinates
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

    def __init__(
        self, name, scale_factor, colour, image, body, label_bottom_right=True
    ):
        self.name = name
        self.scale_factor = scale_factor
        self.body_model = body
        self.originalImage = pygame.image.load(image)
        self.colour = colour or average_colour(self.originalImage)
        self.label_bottom_right = label_bottom_right
        self.positions = collections.deque(maxlen=self.DEQUE_MAXLEN)
        self._screen_positions = collections.deque(maxlen=self.DEQUE_MAXLEN)
        self._bodyToTrack = None
        self._zoomLevel = None
        self._offset = None

    def radius(self, zoom_level, scaled_radius: bool):
        if scaled_radius and self.name != "Center of mass":
            return self.body_model.radius * self.scale_factor * zoom_level
        else:
            return math.log(zoom_level * 10)

    def draw(
        self, window, zoomLevel, offset, bodyToTrack, scaled_radius: bool, tail: bool, label: bool
    ):
        """Draw the body relative to the body to track."""
        self.update_positions(zoomLevel, offset, bodyToTrack)
        if self != bodyToTrack and len(self._screen_positions) > 2 and tail:
            pygame.draw.lines(
                window,
                self.colour,
                closed=False,
                points=self._screen_positions,
                width=1,
            )
        window.blit(
            pygame.transform.scale(
                self.originalImage,
                (
                    self.radius(zoomLevel, scaled_radius) * 2,
                    self.radius(zoomLevel, scaled_radius) * 2,
                ),
            ),
            (
                self._screen_positions[-1][0] - self.radius(zoomLevel, scaled_radius),
                self._screen_positions[-1][1] - self.radius(zoomLevel, scaled_radius),
            ),
        )
        if label:
            self.draw_label(window, zoomLevel, scaled_radius)

    def draw_label(self, window, zoomLevel, scaled_radius: bool):
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
        radius = self.radius(zoomLevel, scaled_radius)
        label_x = self._screen_positions[-1][0] + radius
        label_y = (
            self._screen_positions[-1][1] + radius
            if self.label_bottom_right
            else self._screen_positions[-1][1] - radius
        )
        window.blit(label_zoom, (label_x, label_y))

    def update_positions(self, zoomLevel, offset, bodyToTrack) -> None:
        """Calculate the screen positions relative to the body to track."""
        self.positions.append((self.body_model.position.x, self.body_model.position.y))
        if bodyToTrack == self._bodyToTrack and zoomLevel == self._zoomLevel and offset == self._offset:
            # Zoom level, offset, and body to track didn't change, so just calculate and add the last position
            my_positions = [self.positions[-1]]
            bodyToTrack_positions = [bodyToTrack.positions[-1]]
        else:
            # Zoom level, offset, or body to track changed, so recalculate all positions
            self._screen_positions.clear()
            my_positions = self.positions
            bodyToTrack_positions = bodyToTrack.positions
        positions = relative_coordinates(my_positions, bodyToTrack_positions)
        positions = zoom(positions, self.scale_factor, zoomLevel)
        positions = pan(positions, offset)
        self._screen_positions.extend(positions)
        self._bodyToTrack = bodyToTrack
        self._zoomLevel = zoomLevel
        self._offset = offset

    def get_distance_pixels(self, x: float, y: float) -> float:
        """Get the distance in pixels to the given coordinate"""
        return distance((self._screen_positions[-1][0], self._screen_positions[-1][1]), (x, y))
