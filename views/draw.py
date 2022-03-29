from abc import abstractmethod
from typing import Sequence

import pygame
from pygame.math import Vector2, Vector3
from pygame.surface import Surface


class Drawable:
    """Class to represent drawable objects."""

    def __init__(self, screen_positions: Sequence[Vector3]) -> None:
        self.screen_positions = [Vector2(position.x, position.y) for position in screen_positions]
        self.z = screen_positions[0].z

    def __lt__(self, other: object) -> bool:
        """Return whether this drawable is 'closer' than the other."""
        assert isinstance(other, Drawable)
        return self.z > other.z

    def __eq__(self, other: object) -> bool:
        """Return whether this drawable is equally 'close' as the other."""
        assert isinstance(other, Drawable)
        return self.z == other.z

    @abstractmethod
    def draw(self, window: Surface) -> None:
        """Draw the drawable on the window."""


class Line(Drawable):
    """Class to represent a drawable line."""

    def __init__(self, screen_positions: Sequence[Vector3], colour: tuple[int, int, int]) -> None:
        super().__init__(screen_positions)
        self.colour = colour
        self.width = 5

    def draw(self, window: Surface) -> None:
        """Draw the drawable on the window."""
        pygame.draw.line(
            window, self.colour, start_pos=self.screen_positions[0], end_pos=self.screen_positions[1], width=self.width
        )


class Image(Drawable):
    """Class to represent a drawable image."""

    def __init__(self, screen_position: Vector3, image: Surface) -> None:
        super().__init__([screen_position])
        self.image = image

    def draw(self, window: Surface) -> None:
        """Draw the drawable on the window."""
        window.blit(self.image, (self.screen_positions[0].x, self.screen_positions[0].y))


class Label(Drawable):
    """Class to represent a drawable label."""

    def __init__(self, screen_position: Vector3, label: Surface) -> None:
        super().__init__([screen_position])
        self.label = label

    def draw(self, window: Surface) -> None:
        """Draw the drawable on the window."""
        window.blit(self.label, (self.screen_positions[0].x, self.screen_positions[0].y))
