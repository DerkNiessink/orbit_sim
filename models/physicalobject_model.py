"""Physical object class to represent cellestial bodies."""

from __future__ import annotations

from typing import Sequence

from pygame.math import Vector3


class PhysicalObjectModel:

    gravitational_constant = 6.67408 * 10 ** (-11)
    force_cache: dict[tuple[PhysicalObjectModel, PhysicalObjectModel], Vector3] = dict()
    null_vector = Vector3(0, 0, 0)

    def __init__(
        self,
        initial_position: Vector3,
        initial_velocity: Vector3,
        radius: float,
        mass: float,
    ) -> None:
        self.position = initial_position
        self.velocity = initial_velocity
        self.radius = radius
        self.mass = mass  # kg

    def net_force(self, bodies: Sequence[PhysicalObjectModel]) -> Vector3:
        """Calculate the net force on the body."""
        return sum((self.two_body_force(body) for body in bodies), start=self.null_vector)

    def two_body_force(self, other_body: PhysicalObjectModel) -> Vector3:
        """Return the force between self and other body, from the cache or calculated."""
        if self == other_body:
            return self.null_vector
        key = (self, other_body) if id(self) < id(other_body) else (other_body, self)
        if key in self.force_cache:
            force = -self.force_cache[key]  # Reverse the force direction
            del self.force_cache[key]  # We need the cached force only once
        else:
            self.force_cache[key] = force = self.calculate_two_body_force(other_body)
        return force

    def calculate_two_body_force(self, other_body: PhysicalObjectModel) -> Vector3:
        """Calculate the force between self and other body."""
        position1, position2 = self.position, other_body.position
        distance = (position2 - position1).length()
        force_direction = (position2 - position1).normalize()
        return force_direction * self.gravitational_constant * self.mass * other_body.mass / (distance ** 2)

    def update_position(self, bodies: Sequence[PhysicalObjectModel], time_step: float) -> None:
        """Update the position of the body."""
        acceleration = self.net_force(bodies) / self.mass
        self.velocity += acceleration * time_step
        self.position += self.velocity * time_step
