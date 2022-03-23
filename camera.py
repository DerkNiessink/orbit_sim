"""Orbit sim camera."""

from typing import Sequence

import pygame
from pygame.math import Vector2, Vector3
from pygame.surface import Surface

from models.time import Time
from models.constellation import Constellation
from constellations.solar_system import AU
from views.physicalobject import PhysicalObjectView
from views.settings import ViewSettings


class Camera:

    MAX_ZOOM_LEVEL = 100000
    MIN_ZOOM_LEVEL = 0.1
    ZOOM_STEP = 1.1
    SECONDS_PER_YEAR = 365.25 * 24 * 60 * 60  # One Julian year conform https://en.wikipedia.org/wiki/Julian_year_(astronomy)

    def __init__(
        self,
        window: Surface,
        constellation_model: Constellation,
        body_viewers: Sequence[PhysicalObjectView],
        time: Time,
    ) -> None:
        self.window = window
        self.constellation_model = constellation_model
        self.body_viewers = body_viewers
        self.background_image = pygame.image.load("resources/stars_background.png")
        self.time = time
        self.settings = ViewSettings(body_viewers[0], 1.0, self.initialOffset())
        self.font = pygame.font.SysFont("monospace", 18)

    def initialOffset(self) -> Vector2:
        """The initial offset for the camera is the center of the window. Panning may change the offset."""
        return Vector2(self.window.get_width() / 2, self.window.get_height() / 2)

    def trackBody(self, position: Vector2) -> None:
        """Track the body closest the the x and y coordinates."""
        sorted_bodies = sorted([(body.get_distance_pixels(position), body) for body in self.body_viewers])
        self.settings.bodyToTrack = sorted_bodies[0][1]
        self.settings.offset = self.initialOffset()

    def zoomIn(self) -> None:
        """Zoom in to a maximum of 0.1."""
        self.settings.zoomLevel = max(self.settings.zoomLevel / self.ZOOM_STEP, self.MIN_ZOOM_LEVEL)

    def zoomOut(self) -> None:
        """Zoom out to a maximum of 10."""
        self.settings.zoomLevel = min(self.settings.zoomLevel * self.ZOOM_STEP, self.MAX_ZOOM_LEVEL)

    def pan(self, delta: Vector2) -> None:
        """Pan the camera."""
        self.settings.offset += delta

    def rotate(self, delta: Vector2) -> None:
        speed_factor = 1/300
        self.settings.normalVector += Vector3(delta.x, delta.y, 0) * speed_factor

    def reset_rotation(self) -> None:
        self.settings.normalVector = Vector3(0, 0, 1)

    def toggle_labels(self) -> None:
        """Toggle the display of labels."""
        self.settings.labels = not self.settings.labels

    def toggle_scaled_radius(self) -> None:
        """Toggle body radius to scale"""
        self.settings.scaled_radius = not self.settings.scaled_radius

    def toggle_tail(self) -> None:
        "Toogle the tail of the bodies"
        self.settings.tail = not self.settings.tail

    def save_screenshot(self) -> None:
        """Save a screenshot of the current screen."""
        pygame.image.save(self.window, "screenshot.png")

    def update(self, elapsed_time: float) -> None:

        # draw background image
        background = pygame.transform.scale(self.background_image, (self.window.get_width(), self.window.get_height()))
        self.window.blit(background, (0, 0))

        # update positions
        for body in self.body_viewers:
            body.update_position()

        # render bodies
        for body in self.body_viewers:
            body.draw(self.window, self.settings)

        # draw the elapsed time in years
        elapsed_years = round(elapsed_time / self.SECONDS_PER_YEAR, 1)
        self.draw_label(f"Elapsed time: {elapsed_years} years", (25, 25))

        # display the spatial scale
        pixel_size = 0.026  # cm
        spatial_scale = round(self.body_viewers[0].scale_factor * AU * self.settings.zoomLevel * pixel_size, 2)
        self.draw_label(f"Spatial scale: {spatial_scale} cm = 1 AU", (25, 48))

        # display the temporal scale, take the average of the maxlen of the deque
        self.temporal_scale = self.time.speedup / (24 * 3600)
        self.draw_label(f"Temporal scale: 1 second = {round(self.temporal_scale, 1)} days", (25, 71))

        # display whether radius is scaled or not
        self.draw_label(f"Bodies to scale: {'Yes' if self.settings.scaled_radius else 'No'}", (25, 94))

    def draw_label(self, text: str, coordinate: tuple[int, int], color=(255, 255, 255)) -> None:
        """Draw the label."""
        label = self.font.render(text, True, color)
        self.window.blit(label, coordinate)
