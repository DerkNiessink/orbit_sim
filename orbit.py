"""Orbit sum main program."""

from re import I
from physicalobject import PhysicalObject
import pygame
from constellations.first_constellation import constellation, general_parameters


width = 1500
height = 800
game_window = pygame.display.set_mode((width, height))

# make background dark gray
game_window.fill((50, 50, 50))
pygame.display.set_caption("orbit simulator")


bodies_list = []
for index, key in enumerate(constellation):
    bodies_list.append(
        PhysicalObject(
            constellation[key]["x"],
            constellation[key]["y"],
            constellation[key]["init_velocity_x"],
            constellation[key]["init_velocity_y"],
            constellation[key]["mass"],
            constellation[key]["colour"],
            constellation[key]["image"],
            scale_factor=general_parameters["scale_factor"],
            time_step=general_parameters["time_step"],
        )
    )


class System:
    def __init__(self):
        pass

    def check(self, body):
        return True

    def update(self, window, bodies):
        for body in bodies:
            if self.check(body):
                self.updateBody(window, body, bodies)

    def updateBody(self, window, body, bodies):
        pass


class CameraSystem(System):
    def __init__(self):
        super().__init__()

    def check(self, body):
        return body.camera is not None

    def updateBody(self, window, body, bodies):

        # set clipping rectangle
        cameraRect = body.camera.rect
        clipRect = pygame.Rect(cameraRect.x, cameraRect.y, cameraRect.w, cameraRect.h)
        window.set_clip(clipRect)

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
        for body in bodies_list:
            body.update_position(bodies_list)
            # render bodies
            body.draw(window, width, height, offsetX, offsetY)

        # unset clipping rectangle
        window.set_clip(None)


class Camera:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.cameraX = 0
        self.cameraY = 0
        self.bodyToTrack = 0

    def setCameraPos(self, x, y):
        self.cameraX = x
        self.cameraY = y

    def trackBody(self, body):
        self.bodyToTrack = body


# Set the body to track
body_to_track = bodies_list[0]

camera = body_to_track.camera = Camera(0, 0, 1500, 800)
body_to_track.camera.trackBody(body_to_track)
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
                sorted_bodies = sorted([(body.get_distance_pixels(*event.pos), body) for body in bodies_list])
                nearest_body = sorted_bodies[0][1]
                nearest_body.camera = camera
                nearest_body.camera.trackBody(nearest_body)

        # update the camera system and draw bodies
        cameraSys.update(game_window, bodies_list)

        pygame.display.update()

    pygame.quit()
