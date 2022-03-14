"""Orbit sim main program."""

import pygame
import sys
import importlib

from models.constellation import Constellation
from models.physicalobject_model import PhysicalObjectModel
from models.time import Time
from physicalobject_views import PhysicalObjectView
from camera import Camera
from event_handler import EventHandler


module_name = sys.argv[1].replace("/", ".").removeprefix(".\\").replace("\\", ".").removesuffix(".py")
constellation_module = importlib.import_module(module_name)
window = pygame.display.set_mode(flags=pygame.RESIZABLE)
pygame.display.set_caption("orbit simulator")
pygame.init()


body_models = []
body_viewers = []
for name, body in constellation_module.constellation.items():
    body_model = PhysicalObjectModel(
        body["x"],
        body["y"],
        body["radius"],
        body["init_velocity_x"],
        body["init_velocity_y"],
        body["mass"],
    )
    body_models.append(body_model)
    body_viewers.append(
        PhysicalObjectView(
            name,
            constellation_module.general_parameters["scale_factor"],
            body.get("colour"),
            body["image"],
            body_model,
        )
    )

constellation_model = Constellation(body_models)

body_viewers.insert(
    0,
    PhysicalObjectView(
        "Center of mass",
        constellation_module.general_parameters["scale_factor"],
        [255, 0, 0],
        "resources/center_of_mass.png",
        constellation_model.center_of_mass,
        label_bottom_right=False,
    ),
)


if __name__ == "__main__":
    clock = pygame.time.Clock()
    time = Time(constellation_module.general_parameters["time_step"])
    camera = Camera(window, constellation_model, body_viewers, time)
    event_handler = EventHandler(camera, time)
    while True:
        clock.tick()

        for _ in range(time.calculations):
            event_handler.handle_events()
            constellation_model.update_positions(time.time_step)
        time.update()

        camera.update(time.elapsed_time)

        pygame.display.update()
