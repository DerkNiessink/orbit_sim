"""Event handler module."""

import sys
from typing import TYPE_CHECKING

import pygame
from pygame.math import Vector2

if TYPE_CHECKING:
    from pygame import EventType
else:
    from pygame.event import EventType

from controller.camera import Camera
from controller.time import Time


class EventHandler:
    """Handle user input in the form of pygame events, such as keyboard and mouse events."""

    def __init__(self, camera: Camera, time: Time) -> None:
        self.camera = camera
        self.time = time
        self._mouse_button_down_position = Vector2(-100, -100)

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
            case EventType(type=pygame.VIDEORESIZE):  # type: ignore[misc]
                self.camera.resize()
            case EventType(type=pygame.MOUSEBUTTONDOWN, button=1):  # type: ignore[misc]
                self._mouse_button_down_position = Vector2(*event.pos)
            case EventType(type=pygame.MOUSEBUTTONUP, button=1):  # type: ignore[misc]
                mouse_button_up_position = Vector2(*event.pos)
                if (self._mouse_button_down_position - mouse_button_up_position).length() <= 10:
                    self.camera.trackBody(mouse_button_up_position)
            case EventType(type=pygame.MOUSEBUTTONDOWN, button=4):  # type: ignore[misc]
                self.camera.zoomOut()
            case EventType(type=pygame.MOUSEBUTTONDOWN, button=5):  # type: ignore[misc]
                self.camera.zoomIn()
            case EventType(type=pygame.MOUSEMOTION):  # type: ignore[misc]
                if pygame.mouse.get_pressed()[0]:
                    self.camera.pan(Vector2(*event.rel))
                if pygame.mouse.get_pressed()[2]:
                    self.camera.rotate(Vector2(*event.rel))
            case EventType(type=pygame.KEYDOWN, key=pygame.K_g):  # type: ignore[misc]
                self.camera.save_gif()
            case EventType(type=pygame.KEYDOWN, key=pygame.K_l):  # type: ignore[misc]
                self.camera.toggle_labels()
            case EventType(type=pygame.KEYDOWN, key=pygame.K_s):  # type: ignore[misc]
                if event.mod == pygame.KMOD_NONE:
                    self.camera.toggle_scaled_radius()
                elif event.mod & pygame.KMOD_SHIFT:
                    self.camera.save_screenshot()
            case EventType(type=pygame.KEYDOWN, key=pygame.K_t):  # type: ignore[misc]
                self.camera.toggle_tail()
            case EventType(type=pygame.KEYDOWN, key=pygame.K_UP):  # type: ignore[misc]
                self.time.faster()
            case EventType(type=pygame.KEYDOWN, key=pygame.K_DOWN):  # type: ignore[misc]
                self.time.slower()
            case EventType(type=pygame.KEYDOWN, key=pygame.K_r):  # type: ignore[misc]
                self.camera.reset_rotation()
                self.camera.reset_BodyToTrack()
