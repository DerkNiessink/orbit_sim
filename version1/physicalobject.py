import pyglet
import numpy as np


class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gravitational_const = 1

    def update(self, dt, other_body_position, other_body_mass, mass, init_velocity):

        dst = np.linalg.norm(other_body_position - self.position)
        forceDir = (other_body_position - self.position) / dst
        force = (
            forceDir * self.gravitational_const * mass * other_body_mass / (dst ** 2)
        )
        acceleration = force / mass
        init_velocity = init_velocity + acceleration * dt
        self.velocity_x, self.velocity_y = init_velocity
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def check_bounds(self):
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = 1500 + self.image.width / 2
        max_y = 800 + self.image.height / 2
        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y
