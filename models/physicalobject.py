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
        initial_position: Vector3,
        initial_velocity: Vector3,
        radius: float,
        mass: float,
    ) -> None:
        self.position = initial_position
        self.velocity = initial_velocity
        self.acceleration = self.null_vector
        self.radius = radius  # m
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
        return force_direction * self.mass_product(other_body) / (distance**2)

    @cache
    def mass_product(self, other_body: PhysicalObjectModel) -> float:
        """Return the product of the masses and the gravitational constant."""
        return self.gravitational_constant * self.mass * other_body.mass

    def update_position(self, bodies: Sequence[PhysicalObjectModel], time_step: float) -> None:
        """Update the position of the body."""
        acceleration = self.net_force(bodies) / self.mass
        self.velocity += time_step * ((acceleration + self.acceleration) / 2)
        self.position += time_step * self.velocity + (time_step**2 / 2) * self.acceleration
        self.acceleration = acceleration


class InclinedPhysicalObjectModel(PhysicalObjectModel):
    def __init__(
        self,
        aphelion: float,
        min_orbital_velocity: float,
        inclination: float,
        radius: float,
        mass: float,
    ) -> None:
        position, velocity = elements_to_cartesian(aphelion, min_orbital_velocity, inclination)
        super().__init__(Vector3(position), Vector3(velocity), radius, mass)


def elements_to_cartesian(aphelion, min_orbital_velocity, inclination) -> tuple:
    # convert orbital elements to cartesian position and velocity vectors
    inclination_rad = math.radians(inclination)
    position = (aphelion * math.cos(inclination_rad), 0, aphelion * math.sin(inclination_rad))
    velocity = (0, min_orbital_velocity, 0)
    return position, velocity
