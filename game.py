"""Run this to run the game :)"""

import logging
from collections import namedtuple

import pygame

from world import World

# from pygame.locals import *

Box = namedtuple("Box", ["x", "y", "width", "height"])


class Game:
    def __init__(self):
        self._running = True
        self._screen = None
        self.size = self.width, self.height = 640, 400

        # Surfaces and their position on-screen
        self.surfaces: list[pygame.Surface, tuple[Box]] = [
            (World(), Box(0, 0, 250, 250)),
        ]

    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def process_inputs(self):
        """Checks for inputs from the user; mouse keys etc"""
        mouse_pressed = pygame.mouse.get_pressed
        mouse_position = pygame.mouse.get_pos
        for event in pygame.event.get():
            self.on_event(event)

    def update(self):
        """Update the game. Runs every frame.

        Currently unused but in future this could handle animation frames and
        any cooldowns/timers we may have.
        """
        pass

    def render(self):
        """Draw all the surfaces to the display."""
        self._screen.fill((0, 255, 0))
        for surface in self.surfaces:
            assert type(surface[1]) is Box, f"Expected type Box. Instead got {type(surface[1])}"
            x, y, width, height = surface[1]
            assert x >= 0, f"Surface '{surface.name}' is off the left of the screen!"
            assert y >= 0, f"Surface '{surface.name}' is off the top of the screen!"
            assert x + width <= self.width, f"Surface '{surface.name}' is off the right of the screen!"
            assert y + height <= self.height, f"Surface '{surface.name}' is off the bottom of the screen!"

            self._screen.blit(surface[0].render(), (0, 0), [x, y, width, height])
        pygame.display.update()

    def main_loop(self):
        try:
            self.on_init()
        except Exception:
            self._running = False

        while self._running:
            self.process_inputs()
            self.update()
            self.render()


if __name__ == "__main__":
    game = Game()
    game.main_loop()
