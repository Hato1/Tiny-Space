"""Run this to run the game :)"""

import logging
from enum import Enum

import pygame as pg

import debug
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
        self.box = Box(0, 0, 640, 400)

        self.world: World
        self.sidebar: Sidebar
        self.surfaces: list[Surface] = []

        pg.init()
        self._screen = pg.display.set_mode(self.box.dims, pg.HWSURFACE | pg.DOUBLEBUF | pg.SCALED | pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.main_loop()

    def reset(self):
        """Reset the game and start it again."""
        # The Sidebar occupies the right 30% of the display.
        horizontal_split = int(self.box.width * 0.7)
        sidebar_width = self.box.width - horizontal_split
        self.world = World()
        self.world.graphics.center_box(Box(0, 0, horizontal_split, self.box.height))
        self.sidebar = Sidebar(Box(horizontal_split, 0, sidebar_width, self.box.height))
        self.surfaces = [
            self.world,
            self.sidebar,
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
                debug.debug_1()
            case pg.K_2:
                debug.debug_2()
            case pg.K_3:
                debug.debug_3()

    def process_mouse_input(self, event):
        """Handle a single mouseclick for each surface under the mouse."""
        mouse_position = Point(*event.pos)
        for surface in self.surfaces:
            if relative_position := mouse_position.relative_to(surface.box):
                surface.process_inputs(relative_position)

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
        for event in pg.event.get():
            self.process_input(event)

    def update(self):
        """Update the game. Runs every frame."""
        for surface in self.surfaces:
            surface.update()

    def render(self):
        """Draw all the surfaces to the display."""
        self._screen.fill((0, 0, 0))
        for surface in self.surfaces:
            assert surface.box in self.box, f"{surface.box} does not fit in {self.box}!"
            if surface == self.world:
                # Draw a nice border. Bordered surfaces should ideally be less hacky...
                x, y, width, height = surface.box
                pg.draw.rect(self._screen, (30, 30, 200), (x - 1, y - 1, width + 2, height + 2))
            self._screen.blit(surface.render(), surface.box.top_left)
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
            # Limit FPS to 60
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
