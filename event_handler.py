"""Event handler module."""

import sys
from typing import TYPE_CHECKING

import pygame
from pygame.math import Vector3
if TYPE_CHECKING:
    from pygame import EventType
else:
    from pygame.event import EventType

from camera import Camera
from models.time import Time


class EventHandler:
    """Handle user input in the form of pygame events, such as keyboard and mouse events."""
    def __init__(self, camera: Camera, time: Time) -> None:
        self.camera = camera
        self.time = time
        self._mouse_button_down_position = Vector3(-100, -100, 0)

    def handle_events(self) -> None:
        """Handle the queued pygame events."""
        for event in pygame.event.get():
            self.handle_event(event)

    def handle_event(self, event: EventType) -> None:
        """Handle one pygame event."""
        match event:
            case EventType(type=pygame.QUIT) | EventType(type=pygame.KEYDOWN, key=pygame.K_q):  # type: ignore[misc]
                pygame.quit()
                sys.exit()
            case EventType(type=pygame.MOUSEBUTTONDOWN, button=1):  # type: ignore[misc]
                self._mouse_button_down_position = Vector3(*event.pos, 0)
            case EventType(type=pygame.MOUSEBUTTONUP, button=1):  # type: ignore[misc]
                mouse_button_up_position = Vector3(*event.pos, 0)
                if (self._mouse_button_down_position - mouse_button_up_position).length() <= 10:
                    self.camera.trackBody(mouse_button_up_position)
            case EventType(type=pygame.MOUSEBUTTONDOWN, button=4):  # type: ignore[misc]
                self.camera.zoomOut()
            case EventType(type=pygame.MOUSEBUTTONDOWN, button=5):  # type: ignore[misc]
                self.camera.zoomIn()
            case EventType(type=pygame.MOUSEMOTION):  # type: ignore[misc]
                if pygame.mouse.get_pressed()[0]:
                    self.camera.pan(Vector3(*event.rel, 0))
            case EventType(type=pygame.KEYDOWN, key=pygame.K_l):  # type: ignore[misc]
                self.camera.toggle_labels()
            case EventType(type=pygame.KEYDOWN, key=pygame.K_s):  # type: ignore[misc]
                self.camera.toggle_scaled_radius()
            case EventType(type=pygame.KEYDOWN, key=pygame.K_t):  # type: ignore[misc]
                self.camera.toggle_tail()
            case EventType(type=pygame.KEYDOWN, key=pygame.K_UP):  # type: ignore[misc]
                self.time.faster()
            case EventType(type=pygame.KEYDOWN, key=pygame.K_DOWN):  # type: ignore[misc]
                self.time.slower()
