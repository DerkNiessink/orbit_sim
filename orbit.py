import pyglet
import numpy as np
import collections
import shutil
from physicalobject import PhysicalObject
import os

for i in range(10):
    shutil.copy("planets-modified.png", f"resources/planets-modified{i}.png")
game_window = pyglet.window.Window(
    width=1500, height=800, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS
)

pyglet.resource.path = ["resources"]
pyglet.resource.reindex()


Body1 = PhysicalObject(
    x=game_window.width // 2,
    y=game_window.height // 2,
    init_velocity=np.array([0, 0]),
    mass=100000,
    image=pyglet.resource.image("planets-modified0.png"),
)
Body2 = PhysicalObject(
    x=500,
    y=game_window.height // 2,
    init_velocity=np.array([0, 20]),
    mass=1000,
    image=pyglet.resource.image("planets-modified1.png"),
)
Body3 = PhysicalObject(
    x=488,
    y=game_window.height // 2,
    init_velocity=np.array([0, 25]),
    mass=100,
    image=pyglet.resource.image("planets-modified2.png"),
)
Body4 = PhysicalObject(
    x=400,
    y=500,
    init_velocity=np.array([5, 10]),
    mass=100,
    image=pyglet.resource.image("planets-modified3.png"),
)
colours = [(150, 0, 0), (0, 150, 0), (0, 0, 150), (255, 255, 0)]

bodies = [Body1, Body2, Body3]
for game_object in bodies:
    game_window.push_handlers(game_object)


def update(dt):
    for Body in bodies:
        Body.update(dt, bodies)


positions_dict = collections.defaultdict(list)


@game_window.event
def on_draw():
    game_window.clear()

    for index, body in enumerate(bodies):
        x_position, y_position = body.get_position()
        positions_dict["Body%s" % index].append(x_position)
        positions_dict["Body%s" % index].append(y_position)

    for index, key in enumerate(positions_dict):
        tail(positions_dict[key], colours[index])

    for body in bodies:
        body.draw()


def tail(positions, colour):
    colours = [colour for i in range(len(positions) // 2)]
    colours = [item for t in colours for item in t]

    if len(positions) > 5000:
        del colours[0:3]
        del positions[0:2]

    pyglet.graphics.draw(
        len(positions) // 2,
        pyglet.gl.GL_POINTS,
        ("v2f", (positions)),
        ("c3B", (colours)),
    )


@game_window.event
def on_close():
    for i in range(10):
        os.remove(f"resources\planets-modified{i}.png")


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 120)
    pyglet.app.run()
