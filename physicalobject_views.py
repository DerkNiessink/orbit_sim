import collections

import pygame
import numpy as np


class PhysicalObjectView:
    def __init__(self, scale_factor, colour, image, body):
        self.scale_factor = scale_factor
        self.body_model = body
        self.radius = self.body_model.radius * scale_factor
        self.colour = colour
        image = pygame.image.load(image)
        self.originalImage = image
        self.positions = collections.deque(maxlen=7000)

    def change_coord_sys(self, offsetX, offsetY, width, height, zoomLevel):
        """Scale the positions to pixels and set the origin in the center of the camera."""

        # scale to pixels and place origin in the center of the window
        self.pixel_x = self.body_model.x * self.scale_factor + width / 2
        self.pixel_y = self.body_model.y * self.scale_factor + height / 2

        # place the anchorpoint in the center of the image and the image in the center of the camera
        self.x_to_draw = self.pixel_x + (offsetX / zoomLevel) - self.radius
        self.y_to_draw = self.pixel_y + (offsetY / zoomLevel) - self.radius

    def draw(self, window, offsetX, offsetY, width, height, zoomLevel):

        self.change_coord_sys(offsetX, offsetY, width, height, zoomLevel)
        self.positions.append(
            (
                self.x_to_draw + self.radius,
                self.y_to_draw + self.radius,
            )
        )
        if len(self.positions) > 2:
            pygame.draw.lines(
                window,
                self.colour,
                closed=False,
                points=np.array(self.positions) * zoomLevel,
                width=1,
            )
        window.blit(
            pygame.transform.scale(self.originalImage, (self.radius * 2 * zoomLevel, self.radius * 2 * zoomLevel)),
            (self.x_to_draw * zoomLevel, self.y_to_draw * zoomLevel),
        )

    def get_position_pixels(self):
        """Get the position of the body in pixels with origin in the upperleft corner of the window"""
        return np.array([self.body_model.x, self.body_model.y]) * self.scale_factor

    def get_distance_pixels(self, x: float, y: float, zoomLevel: float) -> float:
        """Get the distance in pixels to the given coordinate"""
        return np.sqrt((self.x_to_draw * zoomLevel - x) ** 2 + (self.y_to_draw * zoomLevel - y) ** 2)

    def clear_tail(self):
        """Remove all positions to prepare for a change in camera viewpoint"""
        self.positions.clear()
