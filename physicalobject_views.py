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
    """Zoom the coordinates with a scale factor and a zoom level."""
    return [coordinate * scale_factor * zoom_level for coordinate in coordinates]


def project(coordinates: Sequence[Vector3], normalVector: Vector3) -> list[Vector2]:
    """Project the 3D coordinates onto a 2D plane."""

    a, b, c = 2.1*math.sin(normalVector.x), 2.1*math.sin(normalVector.y), normalVector.z
    return [
        Vector2(coordinate.x - a*(a*coordinate.x+ b*coordinate.y + c*coordinate.z) / math.sqrt(a**2 + b**2 + c**2), 
    coordinate.y - b*(a*coordinate.x+ b*coordinate.y + c*coordinate.z) / math.sqrt(a**2 + b**2 + c**2)) 
    for coordinate in coordinates
    ]

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
    """Data class to hold settings that determine how the simulation looks."""
    bodyToTrack: PhysicalObjectView
    zoomLevel: float = 1.0
    offset: Vector2 = Vector2(0, 0)
    normalVector: Vector3 = Vector3(0, 0, 1)
    scaled_radius: bool = False
    tail: bool = False
    labels: bool = False

    def copy(self) -> ViewSettings:
        """Return a copy of the settings."""
        return ViewSettings(
            self.bodyToTrack, self.zoomLevel, self.offset.copy(), self.scaled_radius, self.tail, self.labels
        )

    def tail_settings_changed(self, other_settings: ViewSettings) -> bool:
        """Return whether any settings that determine the tail changed."""
        return (
            other_settings.bodyToTrack != self.bodyToTrack
            or other_settings.zoomLevel != self.zoomLevel
            or other_settings.offset != self.offset
            or other_settings.tail != self.tail
            or other_settings.normalVector != self.normalVector
        )


class PhysicalObjectView:
    def __init__(
        self,
        name: str,
        scale_factor: float,
        colour: tuple[int, int, int],
        image: Path,
        font: pygame.SysFont,
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
        self._previous_settings = ViewSettings(self)

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
        if settings.tail and settings.tail_settings_changed(self._previous_settings):
            # We're displaying the tail and settings that determine the tail have changed, so recalculate all positions
            self._screen_positions.clear()
            my_positions: Sequence[Vector3] = self.positions
            bodyToTrack_positions: Sequence[Vector3] = settings.bodyToTrack.positions
        else:
            # We're not displaying the tail or the display parameters have not changed, so only calculate the new point
            my_positions = [self.positions[-1]]
            bodyToTrack_positions = [settings.bodyToTrack.positions[-1]]
        positions_3d = relative_coordinates(my_positions, bodyToTrack_positions)
        positions_2d = project(positions_3d, settings.normalVector)
        positions_2d = zoom(positions_2d, self.scale_factor, settings.zoomLevel)
        positions_2d = pan(positions_2d, settings.offset)
        self._screen_positions.extend(positions_2d)
        self._previous_settings = settings.copy()

    def get_distance_pixels(self, position: Vector2) -> float:
        """Get the distance in pixels to the given coordinate"""
        return (self._screen_positions[-1] - position).length()
