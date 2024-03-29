"""Run this to run the game :)"""

import logging
from enum import Enum

import pygame as pg

from helpers import Box, Point
from sidebar import Sidebar
from templates import Surface
from world import World


class State(Enum):
    RUNNING = 1
    QUITTING = 2
    RESTARTING = 3


class Game:
    def __init__(self):
        logging.info("Starting game...")
        self.state = State.RESTARTING
        self._screen = None
        self.size = self.width, self.height = 640, 400

        # Surfaces and their position on-screen
        self.surfaces: list[tuple[Surface, Box]] = []

        pg.init()
        self._screen = pg.display.set_mode(self.size, pg.HWSURFACE | pg.DOUBLEBUF | pg.SCALED | pg.RESIZABLE)
        self.main_loop()

    def reset(self):
        """Reset the game and start it again."""

        # The Sidebar occupies the right 30% of the display.
        horizontal_split = int(self.width * 0.7)
        sidebar_width = self.width - horizontal_split
        self.surfaces = [
            (World(), Box(0, 0, 250, 250)),
            (Sidebar(sidebar_width, self.height), Box(horizontal_split, 0, sidebar_width, self.height)),
        ]
        self.state = State.RUNNING

    def process_key_input(self, event):
        """Handle a single keypress"""
        match event.key:
            case pg.K_q:
                self.state = State.QUITTING
            case pg.K_r:
                self.reset()
            # These numbers can be used for Debug commands.
            case pg.K_1:
                logging.info(1)
            case pg.K_2:
                logging.info(2)
            case pg.K_3:
                logging.info(3)

    def process_mouse_input(self, event):
        """Handle a single mouseclick"""
        mouse_position = Point(*event.pos)
        for surface in self.surfaces:
            if surface[1].contains(mouse_position):
                relative_position = mouse_position.relative_to(surface[1])
                surface[0].process_inputs(relative_position)

    def process_input(self, event):
        """Handle a single input."""
        if event.type == pg.QUIT:
            self.state = State.QUITTING
        elif event.type == pg.KEYDOWN:
            self.process_key_input(event)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.process_mouse_input(event)

    def process_inputs(self):
        """Handle all user input since the last time this ran."""
        # mouse_pressed = pg.mouse.get_pressed
        # mouse_position = pg.mouse.get_pos
        for event in pg.event.get():
            self.process_input(event)

    def update(self):
        """Update the game. Runs every frame.

        Currently unused but in future this could handle animation frames and
        any cool-downs/timers we may have.
        """
        pass

    def render(self):
        """Draw all the surfaces to the display."""
        self._screen.fill((0, 255, 0))
        for surface in self.surfaces:
            assert type(surface[1]) is Box, f"Expected type Box. Instead got {type(surface[1])}"
            x, y, width, height = surface[1]
            assert x >= 0, f"Surface {surface[0].get_name()!r} is off-screen at x={x}!"
            assert y >= 0, f"Surface {surface[0].get_name()!r} is off-screen at y={y}!"
            assert x + width <= self.width, f"Surface {surface[0].get_name()!r} is off-screen at x={x+width}!"
            assert y + height <= self.height, f"Surface {surface[0].get_name()!r} is off-screen at y={y+height}!"

            self._screen.blit(surface[0].render(), (x, y))
        pg.display.update()

    def main_loop(self):
        while True:
            if self.state == State.RUNNING:
                self.process_inputs()
                self.update()
                self.render()
            elif self.state is State.RESTARTING:
                self.reset()
            elif self.state is State.QUITTING:
                logging.info("Quitting.")
                return


if __name__ == "__main__":
    game = Game()
