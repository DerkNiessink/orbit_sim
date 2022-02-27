"""Orbit sim main program."""

import pygame

from constellations.first_constellation import constellation, general_parameters
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


class CameraSystem:
    def __init__(self):
        self.elapsed_time_to_draw = 0

    def check(self, body):
        return body.camera is not None

    def update(self, window, bodies):
        for body in bodies:
            if self.check(body):
                self.updateBody(window, body)

    def updateBody(self, window, body):

        cameraRect = body.camera.rect

        # calculate offsets
        offsetX = cameraRect.x + cameraRect.w / 2 - body.camera.cameraX
        offsetY = cameraRect.y + cameraRect.h / 2 - body.camera.cameraY
        # fill camera background black
        window.fill((0, 0, 0))

        # update camera if tracking a body
        if body.camera.bodyToTrack is not None:
            trackedBody = body.camera.bodyToTrack
            x, y = trackedBody.get_position_pixels()
            body.camera.cameraX = x + width / 2
            body.camera.cameraY = y + height / 2

        # update the positions for each body
        for body in body_models:
            body.update_position(body_models)

        # render bodies
        for body in body_viewers:
            body.draw(window, offsetX, offsetY, width, height)

        # draw the elapsed time in steps of 10 days
        if int(elapsed_time) % 10 == 0:
            self.elapsed_time_to_draw = elapsed_time
        if elapsed_time < 365:
            label = font.render(
                f"Elapsed time: {int(self.elapsed_time_to_draw)} days",
                1,
                (255, 255, 255),
            )
        else:
            label = font.render(
                f"Elapsed time: {round(int(self.elapsed_time_to_draw) / 365, 1)} yr",
                1,
                (255, 255, 255),
            )
        game_window.blit(label, (25, 25))

        # unset clipping rectangle
        window.set_clip(None)


class Camera:
    def __init__(self, x, y, w, h, body):
        self.rect = pygame.Rect(x, y, w, h)
        self.bodyToTrack = body
        self.cameraX, self.cameraY = 0, 0

    def setCameraPos(self, x, y):
        self.cameraX = x
        self.cameraY = y

    def trackBody(self, body):
        self.bodyToTrack = body


# Set the body to track
body_to_track = body_viewers[0]

camera = body_to_track.camera = Camera(0, 0, 1500, 800, body_to_track)
cameraSys = CameraSystem()

if __name__ == "__main__":
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Move the camera to the body nearest to the mouse click
                sorted_bodies = sorted(
                    [
                        (body.get_distance_pixels(*event.pos), body)
                        for body in body_viewers
                    ]
                )
                nearest_body = sorted_bodies[0][1]
                nearest_body.camera = camera
                nearest_body.camera.trackBody(nearest_body)
                for body in body_viewers:
                    body.clear_tail()

        # keep track of the elapsed time in days
        elapsed_time += general_parameters["time_step"] / (3600 * 24)

        # update the camera system and draw bodies
        cameraSys.update(game_window, body_viewers)

        pygame.display.update()

    pygame.quit()
