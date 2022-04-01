import collections
import functools
import math
import typing
from pathlib import Path
from typing import Sequence

import pygame
from pygame.math import Vector2, Vector3

if typing.TYPE_CHECKING:
    from pygame import SysFont
else:
    from pygame.font import SysFont

from models.physicalobject import PhysicalObjectModel

from .draw import Drawable, Image, Label, Line
from .settings import ViewSettings


def zoom(coordinates: Sequence[Vector3], scale_factor: float, zoom_level: float) -> list[Vector3]:
    """Zoom the coordinates with a scale factor and a zoom level."""
    return [coordinate * scale_factor * zoom_level for coordinate in coordinates]


def rotate(coordinates: Sequence[Vector3], x_rotation: float, y_rotation: float) -> list[Vector3]:
    return [coordinate.rotate_x(x_rotation).rotate_y(y_rotation) for coordinate in coordinates]


def relative_coordinates(coordinates: Sequence[Vector3], origin: Sequence[Vector3]) -> list[Vector3]:
    """Transform the coordinates into coordinates relative to the origin."""
    return [coordinate - origin for coordinate, origin in zip(coordinates, origin)]


def pan(coordinates: list[Vector3], offset: Vector2) -> list[Vector3]:
    """Pan the coordinates with the given offset."""
    return [coordinate + Vector3(offset.x, offset.y, 0) for coordinate in coordinates]


class PhysicalObjectView:
    def __init__(
        self,
        name: str,
        scale_factor: float,
        colour: tuple[int, int, int],
        image: Path,
        font: SysFont,
        body: PhysicalObjectModel,
        tail_length: int,
        label_bottom_right=True,
    ) -> None:
        self.name = name
        self.scale_factor = scale_factor
        self.body_model = body
        self.originalImage = pygame.image.load(image).convert_alpha()
        self.colour = colour or pygame.transform.average_color(self.originalImage)
        self.label = font.render(f"{self.name}", True, (255, 255, 255))
        self.label_bottom_right = label_bottom_right
        self.positions: collections.deque[Vector3] = collections.deque(maxlen=5000)
        self._screen_positions: collections.deque[Vector3] = collections.deque(maxlen=tail_length)
        self._previous_settings = ViewSettings(self)

    def radius(self, zoom_level: float, scaled_radius: bool):
        if scaled_radius and self.name != "Center of mass":
            return self.body_model.radius * self.scale_factor * zoom_level
        else:
            return math.log(zoom_level * 10)

    def drawables(self, settings: ViewSettings) -> Sequence[Drawable]:
        """Return the drawables."""
        radius = self.radius(settings.zoomLevel, settings.scaled_radius)
        current_position = self._screen_positions[-1]
        image_position = Vector3(current_position.x - radius, current_position.y - radius, current_position.z)
        drawables: list[Drawable] = [Image(image_position, self.scaled_image(radius))]
        if settings.labels:
            label_position = Vector3(
                current_position.x + radius,
                current_position.y + radius if self.label_bottom_right else current_position.y - radius,
                current_position.z,
            )
            drawables.append(Label(label_position, self.label))
        if settings.tail:
            for index in range(len(self._screen_positions) - 1):
                drawables.append(Line((self._screen_positions[index], self._screen_positions[index + 1]), self.colour))
        return drawables

    @functools.lru_cache(maxsize=20)
    def scaled_image(self, radius: float):
        """Return the scaled image."""
        return pygame.transform.scale(self.originalImage, (radius * 2, radius * 2))

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
        positions = relative_coordinates(my_positions, bodyToTrack_positions)
        positions = rotate(positions, settings.x_rotation, settings.y_rotation)
        positions = zoom(positions, self.scale_factor, settings.zoomLevel)
        positions = pan(positions, settings.offset)
        self._screen_positions.extend(positions)
        self._previous_settings = settings.copy()

    def get_distance_pixels(self, position: Vector2) -> float:
        """Get the distance in pixels to the given coordinate."""
        return (Vector2(self._screen_positions[-1].x, self._screen_positions[-1].y) - position).length()
