import pyglet
from version1.objects import Planet, Star
from pyglet_gui.manager import Manager
from pyglet_gui.containers import VerticalContainer
from pyglet_gui.sliders import HorizontalSlider
from pyglet_gui.theme import Theme


game_window = pyglet.window.Window(
    width=1500, height=800, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS
)

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


theme = Theme(
    {
        "font": "Lucida Grande",
        "font_size": 12,
        "text_color": [255, 255, 255, 255],
        "gui_color": [255, 0, 0, 255],
        "slider": {
            "knob": {"image": {"source": "slider-knob.png"}, "offset": [-5, -11]},
            "padding": [8, 8, 8, 8],
            "step": {"image": {"source": "slider-step.png"}, "offset": [-2, -8]},
            "bar": {
                "image": {
                    "source": "slider-bar.png",
                    "frame": [8, 8, 8, 0],
                    "padding": [8, 8, 8, 8],
                }
            },
        },
    },
    resources_path="",
)

gui_window = pyglet.window.Window(
    width=500, height=500, style=pyglet.window.Window.WINDOW_STYLE_DEFAULT
)
batch = pyglet.graphics.Batch()


@gui_window.event
def on_draw():
    gui_window.clear()
    batch.draw()


Manager(
    VerticalContainer([HorizontalSlider(), HorizontalSlider(steps=10)]),
    window=gui_window,
    batch=batch,
    theme=theme,
)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 120)
    pyglet.app.run()
