import pyglet
import math
import numpy as np
import pyglet.resource


class PhysicalObject(pyglet.sprite.Sprite):
    @classmethod
    def from_json(cls, json):
        """Create a physical object from a JSON fragment."""
        x = json["x"]
        y = json["y"]
        init_velocity = np.array([json["init_velocity_x"], json["init_velocity_y"]])
        mass = json["mass"]
        image = pyglet.resource.image(json["image"])
        return cls(init_velocity=init_velocity, mass=mass, image=image, x=x, y=y)

    def __init__(self, init_velocity, mass, image, *args, **kwargs):
        image.width = image.height = math.log(mass)
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

        super().__init__(img=image, *args, **kwargs)
        self.gravitational_const = 1
        self.scale = 1
        self.velocity = init_velocity
        self.mass = mass

    def get_position(self):
        return np.array([self.x, self.y])

    def get_mass(self):
        return self.mass

    def update(self, dt, bodies):

        net_force = 0
        for other_body in bodies:
            if other_body is not self:
                other_body_position = other_body.get_position()
                other_body_mass = other_body.get_mass()
                self.position_vector = np.array(self.position)

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

            acceleration = net_force / self.mass

            self.velocity = self.velocity + acceleration * dt
            self.velocity_x, self.velocity_y = self.velocity
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt

        # self.check_bounds()

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
