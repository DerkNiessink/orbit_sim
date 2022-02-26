import collections

import numpy as np
import pygame


class PhysicalObject:
    def __init__(
        self,
        x,
        y,
        init_velocity_x,
        init_velocity_y,
        mass,
        colour,
        image,
        scale_factor,
        time_step,
    ):
        self.x = x
        self.y = y
        self.radius = np.log(mass) ** 3 / 10000
        self.gravitational_const = 6.67408 * 10 ** (-11)
        self.velocity = np.array([init_velocity_x, init_velocity_y])  # m/s
        self.mass = mass  # kg
        self.colour = colour
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(image, (self.radius, self.radius))
        self.positions = collections.deque(maxlen=200)
        self.camera = None
        self.scale_factor = scale_factor
        self.time_step = time_step

    def get_mass(self):
        return self.mass

    def get_position_meters(self):
        "Get the position of the body in meters with origin in the upperleft of the window"
        return np.array([self.x, self.y])

    def get_position_pixels(self):
        "Get the position of the body in pixels with origin in the upperleft of the window"
        return np.array([self.x, self.y]) * self.scale_factor

    def calc_force(self, bodies):
        """calculate the net force on the body"""

        net_force = 0
        for other_body in bodies:
            if other_body is not self:
                other_body_position = other_body.get_position_meters()
                other_body_mass = other_body.get_mass()
                self.position_vector = np.array([self.x, self.y])

                dst = np.linalg.norm(other_body_position - self.position_vector)
                forceDir = (other_body_position - self.position_vector) / dst
                force = (
                    forceDir
                    * self.gravitational_const
                    * self.mass
                    * other_body_mass
                    / (dst ** 2)
                )
                net_force += force
        return net_force

    def update_position(self, bodies):
        net_force = self.calc_force(bodies)
        acceleration = net_force / self.mass
        self.velocity = self.velocity + acceleration * self.time_step
        self.velocity_x, self.velocity_y = self.velocity
        self.x += self.velocity_x * self.time_step
        self.y += self.velocity_y * self.time_step
        self.positions.append(np.array([self.x, self.y]))

    def draw(self, window, width, height, offsetX, offsetY):
        x = self.x * self.scale_factor + width / 2
        y = self.y * self.scale_factor + height / 2

        scaled_positions = []
        if len(self.positions) > 2:
            for position_vector in self.positions:
                position_vector = position_vector * self.scale_factor
                x, y = position_vector
                x += width / 2
                y += height / 2
                scaled_positions.append((x + offsetX, y + offsetY))
            pygame.draw.lines(window, self.colour, False, scaled_positions, 2)
        window.blit(
            self.image,
            (x - self.radius / 2 + offsetX, y - self.radius / 2 + offsetY),
        )
