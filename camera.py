"""Orbit sim camera."""

import pygame

from constellations.first_constellation import AU


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
        self.font = pygame.font.SysFont("monospace", 18)

    def initialOffset(self):
        return (self.window.get_width() / 2, self.window.get_height() / 2)

    def trackBody(self, x: int, y: int) -> None:
        """Track the body closest the the x and y coordinates."""
        sorted_bodies = sorted(
            [(body.get_distance_pixels(x, y), body) for body in self.body_viewers]
        )
        self.bodyToTrack = sorted_bodies[0][1]
        self.offset = self.initialOffset()

    def zoomIn(self):
        """Zoom in to a maximum of 0.1."""
        self.zoomLevel = max(self.zoomLevel / self.ZOOM_STEP, self.MIN_ZOOM_LEVEL)

    def zoomOut(self):
        """Zoom in to a maximum of 10."""
        self.zoomLevel = min(self.zoomLevel * self.ZOOM_STEP, self.MAX_ZOOM_LEVEL)

    def pan(self, dx, dy):
        """Pan the camera."""
        self.offset = (self.offset[0] + dx, self.offset[1] + dy)

    def update(self, elapsed_time, label):

        # fill camera background black
        self.window.fill((0, 0, 0))

        # render bodies
        for body in self.body_viewers:
            body.draw(self.window, self.zoomLevel, self.offset, self.bodyToTrack)

        # draw body labels
        if label == True:
            for body in self.body_viewers:
                body.draw_label(self.window, self.zoomLevel)

        # draw the elapsed time in steps of 10 days
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
