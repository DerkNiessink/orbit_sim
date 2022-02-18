import pyglet
from planet import Planet


game_window = pyglet.window.Window(1500, 800)
pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()


"""img=shapes.Circle(x=100, y=150, radius=100, color=(50, 225, 30))"""

planet = Planet(x=400, y=300)
game_window.push_handlers(planet)


game_objects = [planet]


def update(dt):
    for obj in game_objects:
        obj.update(dt)


@game_window.event
def on_draw():
    game_window.clear()
    planet.draw()


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 120)
    pyglet.app.run()
