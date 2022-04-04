"""Orbit sim camera."""

import threading
from operator import attrgetter
from typing import Sequence

import pygame
from pygame.math import Vector2
from pygame.surface import Surface
from PIL import Image

from models.time import Time
from models.constellation import Constellation
from constellations.solar_system import AU
from views.draw import Drawable
from views.physicalobject import PhysicalObjectView
from views.settings import ViewSettings


class Camera:

    MAX_ZOOM_LEVEL = 100000
    MIN_ZOOM_LEVEL = 0.1
    ZOOM_STEP = 1.1
    SECONDS_PER_YEAR = (
        365.25 * 24 * 60 * 60
    )  # One Julian year conform https://en.wikipedia.org/wiki/Julian_year_(astronomy)

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
        self.background_image = pygame.image.load("resources/stars_background.png").convert_alpha()
        self.scaled_background_image = self.get_scaled_background_image()
        self.time = time
        self.settings = ViewSettings(body_viewers[0], 1.0, self.initialOffset())
        self.font = pygame.font.SysFont("monospace", 18)
        self.images: list[Image.Image] = []
        self.images_to_save = 0
        self.thread: threading.Thread | None = None

    def initialOffset(self) -> Vector2:
        """The initial offset for the camera is the center of the window. Panning may change the offset."""
        return Vector2(self.window.get_width() / 2, self.window.get_height() / 2)

    def trackBody(self, position: Vector2) -> None:
        """Track the body closest to the x and y coordinates."""
        sorted_bodies = sorted(self.body_viewers, key=lambda body: body.get_distance_pixels(position))
        self.settings.bodyToTrack = sorted_bodies[0]
        self.settings.offset = self.initialOffset()

    def reset_BodyToTrack(self):
        """Reset the bodyToTrack to the center of mass"""
        self.settings.bodyToTrack = self.body_viewers[0]

    def zoomIn(self) -> None:
        """Zoom in to a maximum of 0.1."""
        self.settings.zoomLevel = max(self.settings.zoomLevel / self.ZOOM_STEP, self.MIN_ZOOM_LEVEL)

    def zoomOut(self) -> None:
        """Zoom out to a maximum of 10."""
        self.settings.zoomLevel = min(self.settings.zoomLevel * self.ZOOM_STEP, self.MAX_ZOOM_LEVEL)

    def pan(self, delta: Vector2) -> None:
        """Pan the camera."""
        self.settings.offset += delta

    def rotate(self, position: Vector2) -> None:
        """Rotate the camera."""
        speed_factor = 1 / 4
        self.settings.x_rotation += position.y * speed_factor
        self.settings.y_rotation += -position.x * speed_factor

    def reset_rotation(self) -> None:
        """Reset the camera rotation."""
        self.settings.x_rotation = self.settings.y_rotation = 0.0
        self.settings.offset = self.initialOffset()

    def toggle_labels(self) -> None:
        """Toggle the display of labels."""
        self.settings.labels = not self.settings.labels

    def toggle_scaled_radius(self) -> None:
        """Toggle body radius to scale"""
        self.settings.scaled_radius = not self.settings.scaled_radius

    def toggle_tail(self) -> None:
        "Toogle the tail of the bodies"
        self.settings.tail = not self.settings.tail

    def resize(self) -> None:
        """The window was resized by the user."""
        self.scaled_background_image = self.get_scaled_background_image()
        self.settings.offset = self.initialOffset()

    def get_scaled_background_image(self) -> Surface:
        """Return the scaled background image."""
        return pygame.transform.scale(self.background_image, (self.window.get_width(), self.window.get_height()))

    def save_screenshot(self) -> None:
        """Save a screenshot of the current screen."""
        pygame.image.save(self.window, "screenshot.png")

    def save_gif(self) -> None:
        """Save a number of screenshots to create an animated gif."""
        self.images_to_save = 200
        self.images = []

    def update(self, elapsed_time: float) -> None:

        # draw background image
        self.window.blit(self.scaled_background_image, (0,0))

        # update positions
        for body in self.body_viewers:
            body.update_position()

        # render bodies
        drawables: list[Drawable] = []
        for body in self.body_viewers:
            body.update_screen_positions(self.settings)
            drawables.extend(body.drawables(self.settings))
        for drawable in sorted(drawables, key=attrgetter("z")):
            if drawable.in_window(self.window):
                drawable.draw(self.window)

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

        if self.images_to_save > 0:
            size = (self.window.get_width(), self.window.get_height())
            self.images.append(Image.frombytes("RGB", size, pygame.image.tostring(self.window, "RGB")))
            self.draw_label("Recording gif...", (self.window.get_width() // 2 - 20, 50))

            self.images_to_save -= 1
            if self.images_to_save == 0:
                # Save into a GIF file that loops forever
                kwargs = dict(append_images=self.images[1:], save_all=True, duration=30, loop=0)
                self.thread = threading.Thread(target=self.images[0].save, args=("animated.gif",), kwargs=kwargs)
                self.thread.start()

        if self.thread and self.thread.is_alive():
            self.draw_label("Saving gif...", (self.window.get_width() // 2 - 20, 50))

    def draw_label(self, text: str, coordinate: tuple[int, int], color=(255, 255, 255)) -> None:
        """Draw the label."""
        label = self.font.render(text, True, color)
        self.window.blit(label, coordinate)
