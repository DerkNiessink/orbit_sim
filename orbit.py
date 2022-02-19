import pyglet
from version1.objects import CelestialBody
import numpy as np


game_window = pyglet.window.Window(
    width=1500, height=800, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS
)

pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()


inst_speed = np.sqrt(1_000_000 * (1 / 300))
Body1 = CelestialBody(x=350, y=300, init_v_x=0, init_v_y=0, mass=1_000_00000)
Body2 = CelestialBody(x=50, y=100, init_v_x=335.644, init_v_y=0, mass=0.00000001)
game_window.push_handlers(Body1)
game_window.push_handlers(Body2)

game_objects = [Body1, Body2]


def update(dt):
    Body1_position = Body1.get_position()
    Body2_position = Body2.get_position()
    Body1_mass = Body1.get_mass()
    Body2_mass = Body2.get_mass()
    Body1.update(dt, Body2_position, Body2_mass)
    Body2.update(dt, Body1_position, Body1_mass)


@game_window.event
def on_draw():
    game_window.clear()
    Body1.draw()
    Body2.draw()


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 120)
    pyglet.app.run()
