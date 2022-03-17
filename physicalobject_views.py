from __future__ import annotations

import collections
import math
from dataclasses import dataclass
from pathlib import Path
from random import randrange
from typing import cast, Sequence

import pygame
from pygame.math import Vector2, Vector3

from models.physicalobject_model import PhysicalObjectModel


def zoom(coordinates: Sequence[Vector2], scale_factor: float, zoom_level: float) -> list[Vector2]:
    return [coordinate * scale_factor * zoom_level for coordinate in coordinates]

def project(coordinates: Sequence[Vector3]) -> list[Vector2]:
    return [Vector2(x, y) for (x, y, z) in coordinates]

def relative_coordinates(coordinates: Sequence[Vector3], origin: Sequence[Vector3]) -> list[Vector3]:
    """Transform the coordinates into coordinates relative to the origin."""
    return [coordinate - origin for coordinate, origin in zip(coordinates, origin)]

def pan(coordinates: list[Vector2], offset: Vector2) -> list[Vector2]:
    """Pan the coordinates with the given offset."""
    return [coordinate + offset for coordinate in coordinates]


def average_colour(image: pygame.surface.Surface) -> tuple[int, int, int]:
    """Calculate the average colour of an image by sampling a limited number of pixels."""
    width, height = image.get_width(), image.get_height()
    sample_size = round(math.sqrt(width * height))
    random_points = [(randrange(0, width), randrange(0, height)) for _ in range(sample_size)]
    colours = [cast(pygame.Color, image.get_at(point)) for point in random_points]
    colours = [colour for colour in colours if colour.a > 0]  # Ignore transparent pixels
    average_r = round(sum(colour.r for colour in colours) / len(colours))
    average_g = round(sum(colour.g for colour in colours) / len(colours))
    average_b = round(sum(colour.b for colour in colours) / len(colours))
    return (average_r, average_g, average_b)


@dataclass
class ViewSettings:
    bodyToTrack: PhysicalObjectView
    zoomLevel: float = 1.0
    offset: Vector2 = Vector2(0, 0)
    scaled_radius: bool = False
    tail: bool = False
    labels: bool = False


class PhysicalObjectView:
    def __init__(
        self,
        name: str,
        scale_factor: float,
        colour: tuple[int, int, int],
        image: Path,
        font: pygame.font.SysFont,
        body: PhysicalObjectModel,
        tail_length: int,
        label_bottom_right=True,
    ) -> None:
        self.name = name
        self.scale_factor = scale_factor
        self.body_model = body
        self.originalImage = pygame.image.load(image)
        self.colour = colour or average_colour(self.originalImage)
        self.label_font = font
        self.label_bottom_right = label_bottom_right
        self.positions: collections.deque[Vector3] = collections.deque(maxlen=7000)
        self._screen_positions: collections.deque[Vector2] = collections.deque(maxlen=tail_length)
        self._bodyToTrack: PhysicalObjectView | None = None
        self._zoomLevel: float | None = None
        self._offset: Vector2 | None = None
        self._tail: bool | None = None

    def radius(self, zoom_level: float, scaled_radius: bool):
        if scaled_radius and self.name != "Center of mass":
            return self.body_model.radius * self.scale_factor * zoom_level
        else:
            return math.log(zoom_level * 10)

    def draw(self, window, settings: ViewSettings):
        """Draw the body relative to the body to track."""
        self.update_screen_positions(settings)
        if self != settings.bodyToTrack and len(self._screen_positions) > 2 and settings.tail:
            pygame.draw.lines(
                window,
                self.colour,
                closed=False,
                points=[(pos.x, pos.y) for pos in self._screen_positions],
                width=1,
            )
        window.blit(
            pygame.transform.scale(
                self.originalImage,
                (
                    self.radius(settings.zoomLevel, settings.scaled_radius) * 2,
                    self.radius(settings.zoomLevel, settings.scaled_radius) * 2,
                ),
            ),
            (
                self._screen_positions[-1][0] - self.radius(settings.zoomLevel, settings.scaled_radius),
                self._screen_positions[-1][1] - self.radius(settings.zoomLevel, settings.scaled_radius),
            ),
        )
        if settings.labels:
            self.draw_label(window, settings.zoomLevel, settings.scaled_radius)

    def draw_label(self, window, zoomLevel, scaled_radius: bool):
        """Draw a label of the name of the body"""

        label_zoom = self.label_font.render(
            f"{self.name}",
            True,
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

    def update_position(self):
        """Update the list of physical model object positions."""
        self.positions.append(self.body_model.position.copy())

    def update_screen_positions(self, settings: ViewSettings) -> None:
        """Calculate the screen positions relative to the body to track."""
        if settings.tail and self.display_parameters_changed(settings):
            # We're displaying the tail and the display parameters have changed, so recalculate all positions
            self._screen_positions.clear()
            my_positions: Sequence[Vector3] = self.positions
            bodyToTrack_positions: Sequence[Vector3] = settings.bodyToTrack.positions
        else:
            # We're not displaying the tail or the display parameters have not changed, so only calculate the new point
            my_positions = [self.positions[-1]]
            bodyToTrack_positions = [settings.bodyToTrack.positions[-1]]
        positions = relative_coordinates(my_positions, bodyToTrack_positions)
        positions = project(positions)
        positions = zoom(positions, self.scale_factor, settings.zoomLevel)
        positions = pan(positions, settings.offset)
        self._screen_positions.extend(positions)
        self._bodyToTrack = settings.bodyToTrack
        self._zoomLevel = settings.zoomLevel
        self._offset = settings.offset.copy()
        self._tail = settings.tail

    def display_parameters_changed(self, settings: ViewSettings) -> bool:
        """Return whether the display parameters changed."""
        return (
            settings.bodyToTrack != self._bodyToTrack
            or settings.zoomLevel != self._zoomLevel
            or settings.offset != self._offset
            or settings.tail != self._tail
        )

    def get_distance_pixels(self, position: Vector2) -> float:
        """Get the distance in pixels to the given coordinate"""
        return (self._screen_positions[-1] - position).length()
