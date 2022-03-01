"""Orbit sim camera."""

import pygame

from constellations.first_constellation import AU


class Camera:

    MAX_ZOOM_LEVEL = 10000
    MIN_ZOOM_LEVEL = 0.1
    ZOOM_STEP = 1.1

    def __init__(self, window, body_models, body_viewers):
        self.window = window
        self.body_models = body_models
        self.body_viewers = body_viewers
        self.bodyToTrack = body_viewers[0]
        self.zoomLevel = 1
        self.elapsed_time_to_draw = 0
        self.font = pygame.font.SysFont("monospace", 18)

    def trackBody(self, body):
        self.bodyToTrack = body

    def zoomIn(self):
        """Zoom in to a maximum of 0.1."""
        self.zoomLevel = max(self.zoomLevel / self.ZOOM_STEP, self.MIN_ZOOM_LEVEL)

    def zoomOut(self):
        """Zoom in to a maximum of 10."""
        self.zoomLevel = min(self.zoomLevel * self.ZOOM_STEP, self.MAX_ZOOM_LEVEL)

    def update(self, elapsed_time):

        # fill camera background black
        self.window.fill((0, 0, 0))

        # update the positions for each body
        for body in self.body_models:
            body.update_position(self.body_models)

        # update camera
        bodyToTrack_x, BodyToTrack_y = self.bodyToTrack.get_position_pixels()
        width, height = self.window.get_size()

        # render bodies
        for body in self.body_viewers:
            body.draw(
                self.window,
                width,
                height,
                self.zoomLevel,
                bodyToTrack_x,
                BodyToTrack_y,
            )

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
