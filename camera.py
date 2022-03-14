"""Orbit sim camera."""

import pygame

from constellations.solar_system import AU


class Camera:

    MAX_ZOOM_LEVEL = 100000
    MIN_ZOOM_LEVEL = 0.1
    ZOOM_STEP = 1.1

    def __init__(self, window, constellation_model, body_viewers, time):
        self.window = window
        self.constellation_model = constellation_model
        self.body_viewers = body_viewers
        self.bodyToTrack = body_viewers[0]
        self.background_image = pygame.image.load("resources/stars_background.png")
        self.time = time
        self.zoomLevel = 1
        self.offset = self.initialOffset()
        self.elapsed_time_to_draw = 0
        self.show_labels = False
        self.scaled_radius = False
        self.show_tail = False
        self.font = pygame.font.SysFont("monospace", 18)

    def initialOffset(self):
        """The initial offset for the camera is the center of the window. Panning may change the offset."""
        return (self.window.get_width() / 2, self.window.get_height() / 2)

    def trackBody(self, x: int, y: int) -> None:
        """Track the body closest the the x and y coordinates."""
        sorted_bodies = sorted([(body.get_distance_pixels(x, y), body) for body in self.body_viewers])
        self.bodyToTrack = sorted_bodies[0][1]
        self.offset = self.initialOffset()

    def zoomIn(self) -> None:
        """Zoom in to a maximum of 0.1."""
        self.zoomLevel = max(self.zoomLevel / self.ZOOM_STEP, self.MIN_ZOOM_LEVEL)

    def zoomOut(self) -> None:
        """Zoom out to a maximum of 10."""
        self.zoomLevel = min(self.zoomLevel * self.ZOOM_STEP, self.MAX_ZOOM_LEVEL)

    def pan(self, dx: int, dy: int) -> None:
        """Pan the camera."""
        self.offset = (self.offset[0] + dx, self.offset[1] + dy)

    def toggle_labels(self) -> None:
        """Toggle the display of labels."""
        self.show_labels = not self.show_labels

    def toggle_scaled_radius(self) -> None:
        """Toggle body radius to scale"""
        self.scaled_radius = not self.scaled_radius

    def toggle_tail(self) -> None:
        "Toogle the tail of the bodies"
        self.show_tail = not self.show_tail

    def update(self, elapsed_time):

        # draw background image
        background = pygame.transform.scale(self.background_image, (self.window.get_width(), self.window.get_height()))
        self.window.blit(background, (0, 0))

        # update positions
        for body in self.body_viewers:
            body.update_position()

        # render bodies
        for body in self.body_viewers:
            body.draw(
                self.window,
                self.zoomLevel,
                self.offset,
                self.bodyToTrack,
                self.scaled_radius,
                self.show_tail,
                self.show_labels,
            )

        # draw the elapsed time in steps of 10 days
        elapsed_time = elapsed_time / (2400 * 36)  # Convert seconds to days
        if int(elapsed_time) % 10 == 0:
            self.elapsed_time_to_draw = elapsed_time
        if elapsed_time < 600:
            elapsed_time_text = f"{int(self.elapsed_time_to_draw)} days"
        else:
            elapsed_time_text = f"{round(int(self.elapsed_time_to_draw) / 365.25, 1)} years"
        self.draw_label(f"Elapsed time: {elapsed_time_text}", (25, 25))

        # display the spatial scale
        pixel_size = 0.026  # cm
        spatial_scale = round(self.body_viewers[0].scale_factor * AU * self.zoomLevel * pixel_size, 2)
        self.draw_label(f"Spatial scale: {spatial_scale} cm = 1 AU", (25, 48))

        # display the temporal scale, take the average of the maxlen of the deque
        self.temporal_scale = self.time.speedup / (24 * 3600)
        self.draw_label(f"Temporal scale: 1 second = {round(self.temporal_scale, 1)} days", (25, 71))

        # display whether radius is scaled or not
        self.draw_label(f"Bodies to scale: {'Yes' if self.scaled_radius else 'No'}", (25, 94))

    def draw_label(self, text: str, coordinate: tuple[int, int], color=(255, 255, 255)) -> None:
        """Draw the label."""
        label = self.font.render(text, True, color)
        self.window.blit(label, coordinate)
