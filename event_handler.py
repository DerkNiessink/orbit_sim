import sys

import pygame
from pygame.event import EventType

from camera import Camera
from physicalobject_views import distance


class EventHandler:
    """Handle user input in the form of pygame events, such as keyboard and mouse events."""
    def __init__(self, camera: Camera) -> None:
        self.camera = camera
        self._mouse_button_down_pos = (-100, -100)

    def handle_events(self) -> None:
        """Handle the queued pygame events."""
        for event in pygame.event.get():
            self.handle_event(event)

    def handle_event(self, event: EventType) -> None:
        """Handle one pygame event."""
        match event:
            case EventType(type=pygame.QUIT) | EventType(type=pygame.KEYDOWN, key=pygame.K_q):
                pygame.quit()
                sys.exit()
            case EventType(type=pygame.MOUSEBUTTONDOWN, button=1):
                self._mouse_button_down_pos = event.pos
            case EventType(type=pygame.MOUSEBUTTONUP, button=1):
                if distance(self._mouse_button_down_pos, event.pos) <= 10:
                    self.camera.trackBody(*event.pos)
            case EventType(type=pygame.MOUSEBUTTONDOWN, button=4):
                self.camera.zoomOut()
            case EventType(type=pygame.MOUSEBUTTONDOWN, button=5):
                self.camera.zoomIn()
            case EventType(type=pygame.MOUSEMOTION):
                if pygame.mouse.get_pressed()[0]:
                    self.camera.pan(*event.rel)
            case EventType(type=pygame.KEYDOWN, key=pygame.K_l):
                self.camera.toggle_labels()
            case EventType(type=pygame.KEYDOWN, key=pygame.K_s):
                self.camera.toggle_scaled_radius()