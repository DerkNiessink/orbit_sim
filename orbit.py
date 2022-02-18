import pyglet
from version1.objects import Planet, Star


game_window = pyglet.window.Window(1500, 800)
pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()


"""img=shapes.Circle(x=100, y=150, radius=100, color=(50, 225, 30))"""


star = Star(x=500, y=500)
planet = Planet(x=400, y=300)
game_window.push_handlers(planet)
game_window.push_handlers(star)

game_objects = [planet, star]


def update(dt):
    star.update(dt)
    planet.update(dt, star.get_position())


@game_window.event
def on_draw():
    game_window.clear()
    planet.draw()
    star.draw()


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 120)
    pyglet.app.run()
