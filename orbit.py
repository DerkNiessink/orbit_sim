"""Orbit sum main program."""

import json
import sys
from physicalobject import PhysicalObject
import pygame
from constellations.first_constellation import constellation


width = 1500
height = 800
game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption("orbit simulator")
pygame.display.flip()
keys = pygame.key.get_pressed()


# filename = sys.argv[1] if len(sys.argv) > 1 else "constellations/first_constellation.py"
# with open(filename) as json_file:
# data = json.load(json_file)


body_dict = {}
for index, key in enumerate(constellation):
    body_dict["Body%s" % index] = PhysicalObject(
        constellation[key]["x"],
        constellation[key]["y"],
        constellation[key]["init_velocity_x"],
        constellation[key]["init_velocity_y"],
        constellation[key]["mass"],
        constellation[key]["colour"],
        constellation[key]["image"],
    )

bodies_list = []
for body in body_dict:
    bodies_list.append(body_dict[body])


class Camera:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)


if __name__ == "__main__":
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(20)
        game_window.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for body in bodies_list:
            body.update_position(
                bodies_list,
                time_step=3600,
                scale_factor=10000 / (149597870000),
            )
            body.draw(game_window, width, height)

        pygame.display.update()

    pygame.quit()
