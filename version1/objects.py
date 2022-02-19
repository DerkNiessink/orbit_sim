from version1.physicalobject import PhysicalObject
from resources.images import planet_image, star_image, center_im
import numpy as np


class CelestialBody(PhysicalObject):
    def __init__(self, init_v_x, init_v_y, mass, *args, **kwargs):
        super().__init__(img=planet_image, *args, **kwargs)
        self.init_velocity = np.array([init_v_x, init_v_y])
        self.mass = mass

    def get_position(self):
        return np.array([self.x, self.y])

    def get_mass(self):
        return self.mass

    def update(self, dt, other_body_postion, other_body_mass):
        init_velocity = self.init_velocity
        mass = self.mass

        super(CelestialBody, self).update(
            dt, other_body_postion, other_body_mass, mass, init_velocity
        )
        self.check_bounds()


"""
class Center(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(img=center_im, *args, **kwargs)
        self.keys = dict(left=False, right=False, up=False)
        self.rotate_speed = 200.0
        self.speed = 5000

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys["up"] = True
        elif symbol == key.LEFT:
            self.keys["left"] = True
        elif symbol == key.RIGHT:
            self.keys["right"] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys["up"] = False
        elif symbol == key.LEFT:
            self.keys["left"] = False
        elif symbol == key.RIGHT:
            self.keys["right"] = False

    def get_position(self):
        return self.x, self.y

    def update(self, dt):
        super(Center, self).update(dt)
        self.check_bounds()

        if self.keys["left"]:
            self.rotation -= self.rotate_speed * dt
        if self.keys["right"]:
            self.rotation += self.rotate_speed * dt
        if self.keys["up"]:
            angle_radians = -math.radians(self.rotation)
            self.velocity_x = math.cos(angle_radians) * self.speed * dt
            self.velocity_y = math.sin(angle_radians) * self.speed * dt
        if not self.keys["up"]:
            self.velocity_x = 0
            self.velocity_y = 0


class Star(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(img=star_image, *args, **kwargs)
        self.keys = dict(c=False)
        self.rotate_speed = 100

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.keys["c"] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.keys["c"] = False

    def get_position(self):
        return self.x, self.y

    def update(self, dt, star_position, axes):
        super(Star, self).update(dt)
        self.check_bounds()
        center_x, center_y = star_position
        semi_mayor_axis, semi_minor_axis = axes
        self.x = math.sqrt(semi_mayor_axis ** 2 - (semi_minor_axis) ** 2) + center_x
        self.y = center_y
        if not self.keys["c"]:
            self.rotation += self.rotate_speed * dt
"""
