"""Orbit sim camera."""

import pygame

from constellations.solar_system import AU


class Camera:

    MAX_ZOOM_LEVEL = 100000
    MIN_ZOOM_LEVEL = 0.1
    ZOOM_STEP = 1.1

    def __init__(self, window, constellation_model, body_viewers):
        self.window = window
        self.constellation_model = constellation_model
        self.body_viewers = body_viewers
        self.bodyToTrack = body_viewers[0]
        self.zoomLevel = 1
        self.offset = self.initialOffset()
        self.elapsed_time_to_draw = 0
        self.show_labels = False
        self.scaled_radius = False
        self.font = pygame.font.SysFont("monospace", 18)

    def initialOffset(self):
        """The initial offset for the camera is the center of the window. Panning may change the offset."""
        return (self.window.get_width() / 2, self.window.get_height() / 2)

    def trackBody(self, x: int, y: int) -> None:
        """Track the body closest the the x and y coordinates."""
        sorted_bodies = sorted(
            [(body.get_distance_pixels(x, y), body) for body in self.body_viewers]
        )
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

    def update(self, elapsed_time):

        # fill camera background black
        self.window.fill((0, 0, 0))

        # render bodies
        for body in self.body_viewers:
            body.draw(
                self.window,
                self.zoomLevel,
                self.offset,
                self.bodyToTrack,
                self.scaled_radius,
            )

        # draw body labels
        if self.show_labels:
            for body in self.body_viewers:
                body.draw_label(self.window, self.zoomLevel, self.scaled_radius)

        # draw the elapsed time in steps of 10 days
        elapsed_time = elapsed_time / (2400 * 36)  # Convert seconds to days
        if int(elapsed_time) % 10 == 0:
            self.elapsed_time_to_draw = elapsed_time
        if elapsed_time < 365:
            label_time = self.font.render(
                f"Elapsed time: {int(self.elapsed_time_to_draw)} days",
                1,
                (255, 255, 255),
            )
        else:
            label_time = self.font.render(
                f"Elapsed time: {round(int(self.elapsed_time_to_draw) / 365, 1)} yr",
                1,
                (255, 255, 255),
            )
        self.window.blit(label_time, (25, 25))

        # draw the scale on the screen
        pixel_size = 0.026  # cm
        label_zoom = self.font.render(
            f"Scale: {round(self.body_viewers[0].scale_factor * AU * self.zoomLevel * pixel_size, 2)} cm = AU",
            1,
            (255, 255, 255),
        )
        self.window.blit(label_zoom, (25, 48))

        # display whether radius is scaled or not
        if self.scaled_radius == True:
            scaled_radius = "Yes"
        else:
            scaled_radius = "No"
        label_scale = self.font.render(
            f"Bodies to scale: {scaled_radius}",
            1,
            (255, 255, 255),
        )
        self.window.blit(label_scale, (25, 71))
