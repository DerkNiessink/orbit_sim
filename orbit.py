"""Orbit sim main program."""

import pygame

from constellations.first_constellation import constellation, general_parameters, AU
from physicalobject_model import PhysicalObjectModel
from physicalobject_views import PhysicalObjectView
from camera import Camera

width = 1500
height = 800
game_window = pygame.display.set_mode((width, height))

# make background dark gray
game_window.fill((50, 50, 50))
pygame.display.set_caption("orbit simulator")
pygame.init()
keys = pygame.key.get_pressed()
elapsed_time = 0


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

    body_viewers.append(
        PhysicalObjectView(
            name,
            general_parameters["scale_factor"],
            body["colour"],
            body["image"],
            body_model,
        )
    )


camera = Camera(game_window, body_models, body_viewers)

if __name__ == "__main__":
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Move the camera to the body nearest to the mouse click
                sorted_bodies = sorted(
                    [
                        (body.get_distance_pixels(*event.pos), body) for body in body_viewers
                    ]
                )
                camera.trackBody(sorted_bodies[0][1])

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    camera.zoomOut()
                if event.button == 5:
                    camera.zoomIn()

        # keep track of the elapsed time in days
        elapsed_time += general_parameters["time_step"] / (3600 * 24)

        # update the camera system and draw bodies
        camera.update(elapsed_time)

        pygame.display.update()

    pygame.quit()
