import math
import numpy as np
import pygame


class PhysicalObject:
    """
    @classmethod
    def from_json(cls, json):
        x = json["x"]
        y = json["y"]
        init_velocity = np.array([json["init_velocity_x"], json["init_velocity_y"]])
        mass = json["mass"]
        colour = json["colour"]
        return cls(init_velocity=init_velocity, mass=mass, x=x, y=y, colour=colour)
    """

    def __init__(self, x, y, init_velocity_x, init_velocity_y, mass, colour, image):
        self.x = x
        self.y = y
        self.radius = np.log(mass) ** 3 / 10000
        self.gravitational_const = 6.67408 * 10 ** (-11)
        self.velocity = np.array([init_velocity_x, init_velocity_y])  # m/s
        self.mass = mass  # kg
        self.colour = colour
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(image, (self.radius, self.radius))
        self.positions = []

    def get_position(self):
        return np.array([self.x, self.y])

    def get_mass(self):
        return self.mass

    def calc_force(self, bodies, scale_factor):
        """calculate the net force on the body"""
        self.scale_factor = scale_factor
        net_force = 0
        for other_body in bodies:
            if other_body is not self:
                other_body_position = other_body.get_position()
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

    def update_position(self, bodies, time_step, scale_factor):
        net_force = self.calc_force(bodies, scale_factor)
        acceleration = net_force / self.mass
        self.velocity = self.velocity + acceleration * time_step
        self.velocity_x, self.velocity_y = self.velocity
        self.x += self.velocity_x * time_step
        self.y += self.velocity_y * time_step
        self.positions.append(np.array([self.x, self.y]))

    def draw(self, window, width, height):
        x = self.x * self.scale_factor + width / 2
        y = self.y * self.scale_factor + height / 2

        scaled_positions = []
        if len(self.positions) > 2:
            for position_vector in self.positions:
                position_vector = position_vector * self.scale_factor
                x, y = position_vector
                x += width / 2
                y += height / 2
                scaled_positions.append((x, y))
                del scaled_positions[0:-500]
            pygame.draw.lines(window, self.colour, False, scaled_positions, 2)

        window.blit(self.image, (x - self.radius / 2, y - self.radius / 2))
