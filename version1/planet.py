from physicalobject import PhysicalObject
from pyglet.window import key
from resources.resources import planet_image


class Planet(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(img=planet_image, *args, **kwargs)
        self.keys = dict(left=False, right=False, up=False, down=False)

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

    def update(self, dt):
        super(Planet, self).update(dt)

        if self.keys["left"]:
            self.movement -= self.movement_speed * dt
        if self.keys["right"]:
            self.movement += self.movement_speed * dt
