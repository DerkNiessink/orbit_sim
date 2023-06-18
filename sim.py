"""Orbit sim main program."""

import sys
from pathlib import Path
import json

import pygame
from pygame.locals import *
from pygame.math import Vector3

from models.constellation import Constellation
from models.physicalobject import InclinedPhysicalObjectModel, PhysicalObjectModel
from controller.time import Time
from views.physicalobject import PhysicalObjectView
from controller.camera import Camera
from controller.event_handler import EventHandler
from resources.image_type import images


def orbit_sim(module_name):
    with open(module_name) as json_file:
        constellation_module = json.load(json_file)

    window = pygame.display.set_mode(flags=pygame.RESIZABLE)
    window.set_alpha(None)
    pygame.display.set_caption("orbit simulator")
    pygame.init()
    font = pygame.font.SysFont("monospace", 15)

    body_models = []
    body_viewers = []
    for name, body in constellation_module["Constellation"].items():
        aphelion = body.get("aphelion")
        if aphelion:
            body_model = InclinedPhysicalObjectModel(
                aphelion, body["min_orbital_velocity"], body["inclination"], body["radius"], body["mass"]
            )
        else:
            body_model = PhysicalObjectModel(
                Vector3(body["init_position"]),
                Vector3(body["init_velocity"]),
                body["radius"],
                body["mass"],
            )
        body_models.append(body_model)
        body_viewers.append(
            PhysicalObjectView(
                name,
                constellation_module["scale_factor"],
                body.get("colour"),
                images[body["type"]],
                font,
                body_model,
                body.get("tail_length", 5000),
            )
        )

    constellation_model = Constellation(body_models)

    body_viewers.insert(
        0,
        PhysicalObjectView(
            "Center of mass",
            constellation_module["scale_factor"],
            (255, 0, 0),
            Path("resources/center_of_mass.png"),
            font,
            constellation_model.center_of_mass,
            500,
            label_bottom_right=False,
        ),
    )

    clock = pygame.time.Clock()
    time = Time(constellation_module["time_step"])
    camera = Camera(window, body_viewers, time)
    event_handler = EventHandler(camera, time)
    while True:
        clock.tick()

        for _ in range(time.calculations):
            event_handler.handle_events()
            constellation_model.update_positions(time.time_step)
        time.update()

        camera.update(time.elapsed_time)

        pygame.display.update()


if __name__ == "__main__":
    orbit_sim(sys.argv[1])
