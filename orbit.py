import pyglet
from version1.objects import Planet, Star
from pyglet_gui.theme import Theme
from pyglet_gui.gui import Label


theme = pyglet_gui.theme.Theme(
    {"font": "Lucida Grande", "font_size": 12, "text_color": [255, 0, 0, 255]},
    resources_path="",
)
image1 = pyglet.image.AbstractImage(width=30, height=30)
image2 = pyglet.image.AbstractImage(width=30, height=30)
game_window = pyglet.window.Window(
    width=1500, height=800, style=pyglet.window.Window.WINDOW_STYLE_TOOL
)
controller = pyglet.gui.WidgetBase(20, 20, 200, 200)
pushbutton = pyglet.gui.PushButton(50, 50, image1, image2)

pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()


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
    star_x, star_y = star.get_position()
    semi_mayor_axis, semi_minor_axis = planet.get_axes()
    ellipse = pyglet.shapes.Ellipse(star_x, star_y, semi_mayor_axis, semi_minor_axis)
    ellipse.draw()
    planet.draw()
    star.draw()


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 120)
    pyglet.app.run()
