"""Physical object class to represent cellestial bodies."""

import numpy as np
from pygame import math


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
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = math.Vector2(init_velocity_x, init_velocity_y)  # m/s
        self.mass = mass  # kg

    def position(self):
        """Get the position of the body in meters."""
        return math.Vector2(self.x, self.y)

    def force(self, bodies):
        """Calculate the net force on the body."""
        return sum(
            (self.force_between_two_bodies(body) for body in bodies),
            start=math.Vector2(0, 0),
        )

    def force_between_two_bodies(self, other_body):
        """Calculate the force between this body and another body."""
        if self is other_body:
            return math.Vector2(0, 0)
        self_position = self.position()
        other_body_position = other_body.position()
        distance = (other_body_position - self_position).length()
        force_direction = (other_body_position - self_position).normalize()
        return (
            force_direction
            * self.gravitational_constant
            * self.mass
            * other_body.mass
            / (distance ** 2)
        )

    def update_position(self, bodies, time_step):
        """Update the position of the body."""
        net_force = self.force(bodies)
        acceleration = net_force / self.mass
        self.velocity = self.velocity + acceleration * time_step
        self.velocity_x, self.velocity_y = self.velocity
        self.x += self.velocity_x * time_step
        self.y += self.velocity_y * time_step
