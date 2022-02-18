from version1.physicalobject import PhysicalObject
from pyglet.window import key
from resources.images import planet_image, star_image
import math
import time
import pyglet


class Planet(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(img=planet_image, *args, **kwargs)
        self.keys = dict(left=False, right=False, up=False, down=False, c=False)
        self.rotate_speed = 100
        self.semi_mayor_axis = 400
        self.semi_minor_axis = 200

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.keys["left"] = True
        elif symbol == key.RIGHT:
            self.keys["right"] = True
        elif symbol == key.C:
            self.keys["c"] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.C:
            self.keys["c"] = False
        elif symbol == key.LEFT:
            self.keys["left"] = False
        elif symbol == key.RIGHT:
            self.keys["right"] = False

    def get_positions(self):
        return self.x, self.y

    def get_axes(self):
        return self.semi_mayor_axis, self.semi_minor_axis

    def update(self, dt, location):
        super(Planet, self).update(dt)
        self.check_bounds()

        if self.keys["left"]:
            self.rotation -= self.rotate_speed * dt
        if self.keys["right"]:
            self.rotation += self.rotate_speed * dt
        if not self.keys["c"]:
            location_x, location_y = location
            angle = time.time() / 3
            self.x = self.semi_mayor_axis * math.cos(angle) + location_x
            self.y = self.semi_minor_axis * math.sin(angle) + location_y
            self.rotation += self.rotate_speed * dt


class Star(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(img=star_image, *args, **kwargs)
        self.keys = dict(left=False, right=False, up=False, down=False)
        self.rotate_speed = 200.0
        self.speed = 5000

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys["up"] = True
        elif symbol == key.LEFT:
            self.keys["left"] = True
        elif symbol == key.RIGHT:
            self.keys["right"] = True
        elif symbol == key.DOWN:
            self.keys["down"] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys["up"] = False
        elif symbol == key.LEFT:
            self.keys["left"] = False
        elif symbol == key.RIGHT:
            self.keys["right"] = False
        elif symbol == key.DOWN:
            self.keys["down"] = False

    def get_position(self):
        return self.x, self.y

    def update(self, dt):
        super(Star, self).update(dt)
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
