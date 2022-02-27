import pygame
import numpy as np


class PhysicalObjectView:
    def __init__(self, scale_factor, colour, image, body):
        self.scale_factor = scale_factor
        self.body_model = body
        self.colour = colour
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(
            image, (self.body_model.radius, self.body_model.radius)
        )
        self.camera = None

    def change_coord_sys(self, offsetX, offsetY, width, height):
        """scale the positions to pixels and set the origin in the center of the camera."""

        self.scaled_positions = []
        for position_vector in self.body_model.positions:
            position_vector = position_vector * self.scale_factor
            x, y = position_vector
            x += width / 2
            y += height / 2
            self.scaled_positions.append((x + offsetX, y + offsetY))

        # scale to pixels and place origin in the center of the window
        self.pixel_x = self.body_model.x * self.scale_factor + width / 2
        self.pixel_y = self.body_model.y * self.scale_factor + height / 2

        # place the anchorpoint in the center of the image and the image in the center of the camera
        self.x_to_draw = self.pixel_x - self.body_model.radius / 2 + offsetX
        self.y_to_draw = self.pixel_y - self.body_model.radius / 2 + offsetY

    def draw(self, window, offsetX, offsetY, width, height):

        self.change_coord_sys(offsetX, offsetY, width, height)
        if len(self.body_model.positions) > 2:
            pygame.draw.lines(window, self.colour, False, self.scaled_positions, 2)

        window.blit(
            self.image,
            (
                self.x_to_draw,
                self.y_to_draw,
            ),
        )

    def get_position_pixels(self):
        """Get the position of the body in pixels with origin in the upperleft corner of the window"""
        return np.array([self.body_model.x, self.body_model.y]) * self.scale_factor

    def get_distance_pixels(self, x: float, y: float) -> float:
        """Get the distance in pixels to the given coordinate"""
        return np.sqrt((self.pixel_x - x) ** 2 + (self.pixel_y - y) ** 2)
