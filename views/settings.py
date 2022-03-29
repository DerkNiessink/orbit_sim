from __future__ import annotations

from dataclasses import dataclass
import typing

from pygame.math import Vector2

if typing.TYPE_CHECKING:
    from .physicalobject import PhysicalObjectView


@dataclass
class ViewSettings:
    """Data class to hold settings that determine how the simulation looks."""

    bodyToTrack: PhysicalObjectView
    zoomLevel: float = 1.0
    offset: Vector2 = Vector2(0, 0)
    x_rotation: float = 0.0
    y_rotation: float = 0.0
    scaled_radius: bool = False
    tail: bool = False
    labels: bool = False

    def copy(self) -> ViewSettings:
        """Return a copy of the settings."""
        return ViewSettings(
            self.bodyToTrack,
            self.zoomLevel,
            self.offset.copy(),
            self.x_rotation,
            self.y_rotation,
            self.scaled_radius,
            self.tail,
            self.labels,
        )

    def tail_settings_changed(self, other_settings: ViewSettings) -> bool:
        """Return whether any settings that determine the tail changed."""
        return (
            other_settings.bodyToTrack != self.bodyToTrack
            or other_settings.zoomLevel != self.zoomLevel
            or other_settings.offset != self.offset
            or other_settings.tail != self.tail
            or other_settings.x_rotation != self.x_rotation
            or other_settings.y_rotation != self.y_rotation
        )
