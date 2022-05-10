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
        self._hash_value = hash((self.screen_positions[0].x, self.screen_positions[0].y))

    def in_window(self, width: int, height: int) -> bool:
        """Return whether the drawable is visible."""
        for screen_position in self.screen_positions:
            if 0 < screen_position.x < width and 0 < screen_position.y < height:
                return True
        return False

    def __hash__(self) -> int:
        return self._hash_value

    def __eq__(self, other) -> bool:
        return self.screen_positions[0] == other.screen_positions[0]

    @abstractmethod
    def draw(self, window: Surface) -> None:
        """Draw the drawable on the window."""


class Line(Drawable):
    """Class to represent a drawable line."""

    def __init__(self, screen_positions: Sequence[Vector3], colour: tuple[int, int, int]) -> None:
        super().__init__(screen_positions)
        self.colour = colour
        self.width = 2

    def draw(self, window: Surface, line=pygame.draw.line) -> None:
        """Draw the drawable on the window."""
        start_pos, end_pos = self.screen_positions
        line(window, self.colour, start_pos=start_pos, end_pos=end_pos, width=self.width)


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
