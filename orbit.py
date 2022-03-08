"""Orbit sim main program."""

import pygame

from constellations.binary_star import constellation, general_parameters
from models.physicalobject_model import PhysicalObjectModel
from physicalobject_views import PhysicalObjectView, distance
from models.constellation import Constellation
from camera import Camera


game_window = pygame.display.set_mode(flags=pygame.RESIZABLE)
pygame.display.set_caption("orbit simulator")
pygame.init()
label = False
elapsed_time = 0.0


body_models = []
body_viewers = []
for name, body in constellation.items():
    body_model = PhysicalObjectModel(
        body["x"],
        body["y"],
        body["radius"],
        body["init_velocity_x"],
        body["init_velocity_y"],
        body["mass"],
        general_parameters["time_step"],
    )
    body_models.append(body_model)

    constellation_model = Constellation(body_models)

    body_viewers.append(
        PhysicalObjectView(
            name,
            general_parameters["scale_factor"],
            body.get("colour"),
            body["image"],
            body_model,
        )
    )


camera = Camera(game_window, constellation_model, body_viewers)


if __name__ == "__main__":
    mouse_button_down_pos = (-100, -100)
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick()

        for _ in range(100):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_button_down_pos = (
                        event.pos
                    )  # Keep track of mouse button down to distinguish click from drag
                if (
                    event.type == pygame.MOUSEBUTTONUP
                    and event.button == 1
                    and distance(mouse_button_down_pos, event.pos) <= 10
                ):
                    camera.trackBody(*event.pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        camera.zoomOut()
                    if event.button == 5:
                        camera.zoomIn()

                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                    camera.pan(*event.rel)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    label = not label  # press l to show or unshow body labels

            # keep track of the elapsed time in days
            elapsed_time += general_parameters["time_step"] / (3600 * 24)

            # update the body positions
            constellation_model.update_positions()

        # update the camera system and draw bodies
        camera.update(elapsed_time, label)

        pygame.display.update()

    pygame.quit()
