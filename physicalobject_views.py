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

    def change_coord_sys(self, x, y, offsetX, offsetY, width, height, zoomLevel):
        """Scale the positions to pixels and set the origin in the center of the camera."""

        # scale to pixels and place origin in the center of the window
        self.pixel_x = x * self.scale_factor + width / 2
        self.pixel_y = y * self.scale_factor + height / 2

        # place the anchorpoint in the center of the image and the image in the center of the camera
        x_to_draw = (self.pixel_x + (offsetX / zoomLevel) - self.radius) * zoomLevel
        y_to_draw = (self.pixel_y + (offsetY / zoomLevel) - self.radius) * zoomLevel
        return x_to_draw, y_to_draw

    def draw(self, window, offsetX, offsetY, width, height, zoomLevel):

        # adjust the radius of the body to the zoomlevel
        radius_to_draw = self.radius * zoomLevel

        # remember the positions in world coords
        self.positions.append(
            (
                self.body_model.x,
                self.body_model.y,
            )
        )

        # convert the world coordinates to pixels and scale to the camera and zoomlevel
        scaled_positions = []
        for position in self.positions:
            x_to_draw, y_to_draw = self.change_coord_sys(
                position[0], position[1], offsetX, offsetY, width, height, zoomLevel
            )
            scaled_positions.append((x_to_draw, y_to_draw))

        if len(self.positions) > 2:
            # draw the tail
            pygame.draw.lines(
                window,
                self.colour,
                closed=False,
                # add the radius to draw the tail in the center of the image
                points=np.array(scaled_positions) + radius_to_draw,
                width=1,
            )

            # take the last position in the list
            self.x_to_draw = scaled_positions[-1][0]
            self.y_to_draw = scaled_positions[-1][1]

            # draw the body
            window.blit(
                pygame.transform.scale(
                    self.originalImage,
                    (radius_to_draw * 2, radius_to_draw * 2),
                ),
                (
                    self.x_to_draw,
                    self.y_to_draw,
                ),
            )

    def get_position_pixels(self):
        """Get the position of the body in pixels with origin in the upperleft corner of the window"""
        return np.array([self.body_model.x, self.body_model.y]) * self.scale_factor

    def get_distance_pixels(self, x: float, y: float, zoomLevel: float) -> float:
        """Get the distance in pixels to the given coordinate"""
        return np.sqrt((self.x_to_draw - x) ** 2 + (self.y_to_draw - y) ** 2)

    def clear_tail(self):
        """Remove all positions to prepare for a change in camera viewpoint"""
        self.positions.clear()
