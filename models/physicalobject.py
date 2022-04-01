"""Physical object class to represent cellestial bodies."""

from __future__ import annotations

from functools import cache
from typing import Sequence
import math

from pygame.math import Vector3



class PhysicalObjectModel:

    gravitational_constant = 6.67408 * 10 ** (-11)
    force_cache: dict[tuple[PhysicalObjectModel, PhysicalObjectModel], Vector3] = dict()
    null_vector = Vector3(0, 0, 0)

    def __init__(
        self,
        initial_position,
        initial_velocity,
        inclination: float,
        radius: float,
        mass: float,
    ) -> None:
        

        # If the input was inclination, aphelion and min_orbital_velocity, compute the position and velocity vector 
        if type(initial_position) == float or type(initial_position) == int:
            inclination_rad = math.radians(inclination)
            self.position = Vector3(initial_position * math.cos(inclination_rad), 0, initial_position * math.sin(inclination_rad))
            self.velocity = Vector3(0, initial_velocity, 0)

        # If the input was a vector with type tuple, just convert to pygame.Vector3
        else:
            self.position = Vector3(initial_position)
            self.velocity = Vector3(initial_velocity)

        self.radius = radius # m
        self.mass = mass  # kg
        self.id = id(self)

    def net_force(self, bodies: Sequence[PhysicalObjectModel]) -> Vector3:
        """Calculate the net force on the body."""
        return sum((self.two_body_force(body) for body in bodies), start=self.null_vector)

    def two_body_force(self, other_body: PhysicalObjectModel) -> Vector3:
        """Return the force between self and other body, from the cache or calculated."""
        if self == other_body:
            return self.null_vector
        key = (self, other_body) if self.id < other_body.id else (other_body, self)
        if key in self.force_cache:
            force = -self.force_cache[key]  # Reverse the force direction
            del self.force_cache[key]  # We need the cached force only once
        else:
            self.force_cache[key] = force = self.calculate_two_body_force(other_body)
        return force

    def calculate_two_body_force(self, other_body: PhysicalObjectModel) -> Vector3:
        """Calculate the force between self and other body."""
        vector = other_body.position - self.position
        distance = vector.length()
        force_direction = vector.normalize()
        return force_direction * self.mass_product(other_body) / (distance ** 2)

    @cache
    def mass_product(self, other_body: PhysicalObjectModel) -> float:
        """Return the product of the masses and the gravitational constant."""
        return self.gravitational_constant * self.mass * other_body.mass

    def update_position(self, bodies: Sequence[PhysicalObjectModel], time_step: float) -> None:
        """Update the position of the body."""
        acceleration = self.net_force(bodies) / self.mass
        self.velocity += acceleration * time_step
        self.position += self.velocity * time_step
