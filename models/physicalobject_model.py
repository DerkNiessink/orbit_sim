"""Physical object class to represent cellestial bodies."""

import numpy as np


class PhysicalObjectModel:

    gravitational_constant = 6.67408 * 10 ** (-11)

    def __init__(
        self,
        x,
        y,
        radius,
        init_velocity_x,
        init_velocity_y,
        mass,
        time_step,
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = np.array([init_velocity_x, init_velocity_y])  # m/s
        self.mass = mass  # kg
        self.time_step = time_step

    def position(self):
        """Get the position of the body in meters."""
        return np.array([self.x, self.y])

    def force(self, bodies):
        """Calculate the net force on the body."""
        return sum(self.force_between_two_bodies(body) for body in bodies)

    def force_between_two_bodies(self, other_body):
        """Calculate the force between this body and another body."""
        if self is other_body:
            return 0
        self_position = self.position()
        other_body_position = other_body.position()
        distance = np.linalg.norm(other_body_position - self_position)
        force_direction = (other_body_position - self_position) / distance
        return (
            force_direction
            * self.gravitational_constant
            * self.mass
            * other_body.mass
            / (distance ** 2)
        )

    def update_position(self, bodies):
        """Update the position of the body."""

        if self.mass == 0:
            self.masses = [body.mass for body in bodies[0:-1]]
            center_of_mass = 0
            for index, body_model in enumerate(bodies[0:-1]):

                center_of_mass += (body_model.position() * self.masses[index]) / sum(
                    self.masses
                )
            self.x, self.y = center_of_mass

        else:
            net_force = self.force(bodies[0:-1])
            acceleration = net_force / self.mass
            self.velocity = self.velocity + acceleration * self.time_step
            self.velocity_x, self.velocity_y = self.velocity
            self.x += self.velocity_x * self.time_step
            self.y += self.velocity_y * self.time_step
