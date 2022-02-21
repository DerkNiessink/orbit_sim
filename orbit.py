import pyglet
import numpy as np
import collections
import shutil
from physicalobject import PhysicalObject
import os
import json

"""
pyglet.resource.path = ["resources"]
BATCH = pyglet.graphics.Batch()

play_button = pyglet.resource.image("play_button.png")
play_button.width = play_button.height = 20

button = pyglet.gui.ToggleButton(
    200, 200, pressed=play_button, depressed=play_button, batch=BATCH
)
gui_window = pyglet.window.Window(
    width=500, height=500, style=pyglet.window.Window.WINDOW_STYLE_DEFAULT
)
frame = pyglet.gui.Frame(gui_window, order=2)


@gui_window.event
def on_mouse_press(x, y, button, modifiers):
    if x < 200 and y < 200:
        print("yes")
        return True
    else:
        return False


@gui_window.event
def on_draw():
    BATCH.draw()
"""

for i in range(10):
    shutil.copy("resources/planets-modified.png", f"resources/planets-modified{i}.png")
game_window = pyglet.window.Window(
    width=1500, height=800, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS
)

pyglet.resource.path = ["resources"]
pyglet.resource.reindex()


with open("constellations/first_constellation.json") as json_file:
    data = json.load(json_file)

body_dict = {}
for index, key in enumerate(data):
    body_dict["Body%s" % index] = PhysicalObject.from_json(data[key])

bodies_list = []
for body in body_dict:
    game_window.push_handlers(body_dict[body])
    bodies_list.append(body_dict[body])


def update(dt):
    for Body in bodies_list:
        Body.update(dt, bodies_list)


positions_dict = collections.defaultdict(list)


def tail(positions, colour):
    colours = [colour for i in range(len(positions) // 2)]
    colours = [item for t in colours for item in t]
    if len(positions) > 3000:
        del colours[0:3]
        del positions[0:2]

    pyglet.graphics.draw(
        len(positions) // 2,
        pyglet.gl.GL_POINTS,
        ("v2f", (positions)),
        ("c3B", (colours)),
    )


colours = []
for key in data:
    colours.append(data[key]["colour"])


@game_window.event
def on_draw():
    game_window.clear()

    for index, body in enumerate(bodies_list):
        x_position, y_position = body.get_position()
        positions_dict["Body%s" % index].append(x_position)
        positions_dict["Body%s" % index].append(y_position)

    for index, key in enumerate(positions_dict):
        tail(positions_dict[key], colours[index])

    for body in bodies_list:
        body.draw()


@game_window.event
def on_close():
    for i in range(10):
        os.remove(f"resources\planets-modified{i}.png")


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 120)
    pyglet.app.run()
