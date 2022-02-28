import collections

import pygame
import numpy as np


class PhysicalObjectView:
    def __init__(self, scale_factor, colour, image, body):
        self.scale_factor = scale_factor
        self.body_model = body
        self.colour = colour
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(
            image, (self.body_model.radius * 2, self.body_model.radius * 2)
        )
        self.positions = collections.deque(maxlen=7000)

    def change_coord_sys(self, offsetX, offsetY, width, height):
        """scale the positions to pixels and set the origin in the center of the camera."""

        # scale to pixels and place origin in the center of the window
        self.pixel_x = self.body_model.x * self.scale_factor + width / 2
        self.pixel_y = self.body_model.y * self.scale_factor + height / 2

        # place the anchorpoint in the center of the image and the image in the center of the camera
        self.x_to_draw = self.pixel_x + offsetX - self.body_model.radius
        self.y_to_draw = self.pixel_y + offsetY - self.body_model.radius

    def draw(self, window, offsetX, offsetY, width, height):

        self.change_coord_sys(offsetX, offsetY, width, height)
        self.positions.append(
            (
                self.x_to_draw + self.body_model.radius,
                self.y_to_draw + self.body_model.radius,
            )
        )
        positions = list(self.positions)
        if len(positions) > 3:
            pygame.draw.lines(
                window, self.colour, closed=False, points=positions[1:], width=2
            )
        window.blit(self.image, (self.x_to_draw, self.y_to_draw))

    def get_position_pixels(self):
        """Get the position of the body in pixels with origin in the upperleft corner of the window"""
        return np.array([self.body_model.x, self.body_model.y]) * self.scale_factor

    def get_distance_pixels(self, x: float, y: float) -> float:
        """Get the distance in pixels to the given coordinate"""
        return np.sqrt((self.x_to_draw - x) ** 2 + (self.y_to_draw - y) ** 2)

    def clear_tail(self):
        """Remove all positions to prepare for a change in camera viewpoint"""
        self.positions.clear()
