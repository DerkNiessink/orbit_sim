"""Orbit sim main program."""

import pygame

from constellations.first_constellation import constellation, general_parameters, AU
from physicalobject_model import PhysicalObjectModel
from physicalobject_views import PhysicalObjectView


width = 1500
height = 800
game_window = pygame.display.set_mode((width, height))

# make background dark gray
game_window.fill((50, 50, 50))
pygame.display.set_caption("orbit simulator")
pygame.init()
font = pygame.font.SysFont("monospace", 18)
keys = pygame.key.get_pressed()
elapsed_time = 0


body_models = []
body_viewers = []
for body in constellation:
    body_model = PhysicalObjectModel(
        constellation[body]["x"],
        constellation[body]["y"],
        constellation[body]["init_velocity_x"],
        constellation[body]["init_velocity_y"],
        constellation[body]["mass"],
        general_parameters["time_step"],
    )
    body_models.append(body_model)

    body_viewers.append(
        PhysicalObjectView(
            general_parameters["scale_factor"],
            constellation[body]["colour"],
            constellation[body]["image"],
            body_model,
        )
    )


class Camera:
    def __init__(self, x, y, w, h, body):
        self.zoomLevel = 1
        self.elapsed_time_to_draw = 0
        self.rect = pygame.Rect(x, y, w, h)
        self.bodyToTrack = body

    def trackBody(self, body):
        self.bodyToTrack = body

    def update(self, window):

        # fill camera background black
        window.fill((0, 0, 0))

        # update the positions for each body
        for body in body_models:
            body.update_position(body_models)

        # update camera
        x, y = self.bodyToTrack.get_position_pixels()
        cameraX = x + width / 2
        cameraY = y + height / 2

        # calculate offsets
        offsetX = self.rect.x + self.rect.w / 2 - (cameraX * self.zoomLevel)
        offsetY = self.rect.y + self.rect.h / 2 - (cameraY * self.zoomLevel)

        # render bodies
        for body in body_viewers:
            body.draw(window, offsetX, offsetY, width, height, self.zoomLevel)

        # draw the elapsed time in steps of 10 days
        if int(elapsed_time) % 10 == 0:
            self.elapsed_time_to_draw = elapsed_time
        if elapsed_time < 365:
            label_time = font.render(
                f"Elapsed time: {int(self.elapsed_time_to_draw)} days",
                1,
                (255, 255, 255),
            )
        else:
            label_time = font.render(
                f"Elapsed time: {round(int(self.elapsed_time_to_draw) / 365, 1)} yr",
                1,
                (255, 255, 255),
            )
        game_window.blit(label_time, (25, 25))

        # draw the scale on the screen
        pixel_size = 0.026  # cm
        label_zoom = font.render(
            f"Scale: {round(body_viewers[0].scale_factor * AU * camera.zoomLevel * pixel_size, 2)} cm = AU",
            1,
            (255, 255, 255),
        )
        game_window.blit(label_zoom, (25, 48))


# Set the default body to track
body_to_track = body_viewers[0]
camera = Camera(0, 0, 1500, 800, body_to_track)

if __name__ == "__main__":
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Move the camera to the body nearest to the mouse click
                sorted_bodies = sorted(
                    [
                        (body.get_distance_pixels(*event.pos), body)
                        for body in body_viewers
                    ]
                )
                nearest_body = sorted_bodies[0][1]
                camera.trackBody(nearest_body)
                for body in body_viewers:
                    body.clear_tail()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    # Zoom out
                    camera.zoomLevel += 0.08
                if event.button == 5 and camera.zoomLevel > 0.08:
                    # Zoom in and make sure the zoomlevel is not negative
                    camera.zoomLevel -= 0.08
                for body in body_viewers:
                    body.clear_tail()

        # keep track of the elapsed time in days
        elapsed_time += general_parameters["time_step"] / (3600 * 24)

        # update the camera system and draw bodies
        camera.update(game_window)

        pygame.display.update()

    pygame.quit()
