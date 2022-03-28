import pygame
from pygame.math import Vector2, Vector3


class Drawable:
    """Class to represent drawable objects."""
    def __init__(self, screen_positions: tuple[Vector3, Vector3], colour: pygame.Color) -> None:
        self.start_position = Vector2(screen_positions[0].x, screen_positions[0].y)
        self.end_position = Vector2(screen_positions[1].x, screen_positions[1].y)
        self.z = screen_positions[0].z
        self.colour = colour
        self.width = 5

    def __lt__(self, other: object) -> bool:
        """Return whether this drawable is 'closer' than the other."""
        assert isinstance(other, Drawable)
        return self.z < other.z

    def __eq__(self, other: object) -> bool:
        """Return whether this drawable is equally 'close' as the other."""
        assert isinstance(other, Drawable)
        return self.z == other.z

    def draw(self, window: pygame.Surface) -> None:
        """Draw the drawable on the window."""
        pygame.draw.line(window, self.colour, start_pos=self.start_position, end_pos=self.end_position, width=self.width)
