"""Orbit sim main program."""

import pygame
import sys
import importlib

from models.physicalobject_model import PhysicalObjectModel
from physicalobject_views import PhysicalObjectView, distance
from models.constellation import Constellation
from camera import Camera
from event_handler import EventHandler


module_name = (
    sys.argv[1]
    .replace("/", ".")
    .removeprefix(".\\")
    .replace("\\", ".")
    .removesuffix(".py")
)
print(module_name)
print(sys.argv[1])
constellation_module = importlib.import_module(module_name)
game_window = pygame.display.set_mode(flags=pygame.RESIZABLE)
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

    constellation_model = Constellation(
        body_models, constellation_module.general_parameters["time_step"]
    )

    body_viewers.append(
        PhysicalObjectView(
            name,
            constellation_module.general_parameters["scale_factor"],
            body.get("colour"),
            body["image"],
            body_model,
        )
    )


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
    camera = Camera(game_window, constellation_model, body_viewers)
    event_handler = EventHandler(camera)
    while True:
        clock.tick()

        for _ in range(60):
            event_handler.handle_events()
            constellation_model.update_positions()

        # update the camera system and draw bodies
        camera.update(constellation_model.elapsed_time)

        pygame.display.update()
