from calendar import c
from physicalobject import PhysicalObject
from pyglet.window import key
from resources.images import planet_image
import math
import time


class Planet(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(img=planet_image, *args, **kwargs)
        self.keys = dict(left=False, right=False, up=False, down=False, c=False)
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
        elif symbol == key.C:
            self.keys["c"] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys["up"] = False
        elif symbol == key.LEFT:
            self.keys["left"] = False
        elif symbol == key.RIGHT:
            self.keys["right"] = False
        elif symbol == key.DOWN:
            self.keys["down"] = False
        elif symbol == key.C:
            self.keys["c"] = False

    def update(self, dt):
        super(Planet, self).update(dt)
        self.check_bounds()

        if self.keys["left"]:
            self.rotation -= self.rotate_speed * dt
        if self.keys["right"]:
            self.rotation += self.rotate_speed * dt
        if self.keys["up"]:
            angle_radians = -math.radians(self.rotation)
            self.velocity_x = math.cos(angle_radians) * self.speed * dt
            self.velocity_y = math.sin(angle_radians) * self.speed * dt
        if not self.keys["c"]:
            angle = math.pi * time.time()
            print(time.time())
            self.x = -100 * math.sin(angle) + 1500 / 2
            self.y = 100 * math.cos(angle) + 800 / 2
