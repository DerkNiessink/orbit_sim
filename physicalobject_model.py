"""Physical object class to represent cellestial bodies."""

import numpy as np


class PhysicalObjectModel:
    def __init__(
        self,
        x,
        y,
        init_velocity_x,
        init_velocity_y,
        mass,
        time_step,
    ):
        self.x = x
        self.y = y
        self.radius = np.log(mass) ** 3 / 20000
        self.gravitational_const = 6.67408 * 10 ** (-11)
        self.velocity = np.array([init_velocity_x, init_velocity_y])  # m/s
        self.mass = mass  # kg
        self.time_step = time_step

    def get_mass(self):
        return self.mass

    def get_position_meters(self):
        """Get the position of the body in meters with origin in the upperleft corner of the window"""
        return np.array([self.x, self.y])

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
        """update the position of the body, returns the position in meter with the origin in upperleft corner of the window"""

        net_force = self.calc_force(bodies)
        acceleration = net_force / self.mass
        self.velocity = self.velocity + acceleration * self.time_step
        self.velocity_x, self.velocity_y = self.velocity
        self.x += self.velocity_x * self.time_step
        self.y += self.velocity_y * self.time_step
