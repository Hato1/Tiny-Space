"""Run this to run the game :)"""

import asyncio
import logging
from enum import Enum

import pygame as pg

import config
from tiny_space import debug
from tiny_space.helpers import Point
from tiny_space.sidebar import Sidebar
from tiny_space.templates import GraphicsComponent
from tiny_space.world import World


class State(Enum):
    RUNNING = 1
    QUITTING = 2
    RESTARTING = 3


class Game:
    def __init__(self):
        logging.info("Starting game...")
        self.state = State.RESTARTING

        self.world: World
        self.sidebar: Sidebar
        self.surfaces: list[tuple[Point, GraphicsComponent]] = []

        pg.init()
        pg.display.set_caption("Tiny Space")
        self._screen = pg.display.set_mode(config.RESOLUTION, pg.HWSURFACE | pg.DOUBLEBUF | pg.SCALED | pg.RESIZABLE)
        self.clock = pg.time.Clock()
        asyncio.run(self.main())

    def reset(self):
        """Reset the game and start it again."""
        # The Sidebar occupies the right 30% of the display.
        horizontal_split = int(self._screen.width * 0.7)
        sidebar_width = self._screen.width - horizontal_split

        self.world = World(Point(horizontal_split, self._screen.height))
        assert self.world.surface.get_width() < horizontal_split, "Grid too wide for display area!"
        assert self.world.surface.get_height() < self._screen.height, "Grid too tall for display area!"
        world_pos = self.world.surface.get_rect(center=(horizontal_split // 2, self._screen.height // 2)).topleft

        self.sidebar = Sidebar(Point(sidebar_width, self._screen.height))

        self.surfaces = [
            (Point(*world_pos), self.world),
            (Point(horizontal_split, 0), self.sidebar),
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
        for pos, surface in self.surfaces:
            relative_position = mouse_position - pos
            if surface.surface.get_rect().collidepoint(relative_position):
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

    def update(self, time_delta):
        """Update the game. Runs every frame."""
        for _pos, surface in self.surfaces:
            surface.update(time_delta)

    def render(self):
        """Draw all the surfaces to the display."""
        mouse_pos = Point(*pg.mouse.get_pos())
        self._screen.fill((0, 0, 0))
        for pos, surface in self.surfaces:
            rect = pg.Rect(*pos, *surface.surface.size)
            assert rect in self._screen.get_rect(), f"{rect} does not fit in display!"
            if surface == self.world:
                # Draw a nice border. Bordered surfaces should ideally be less hacky...
                width, height = surface.surface.size
                pg.draw.rect(self._screen, (30, 30, 200), (pos[0] - 1, pos[1] - 1, width + 2, height + 2))
            self._screen.blit(surface.render(mouse_pos - pos), pos)
        pg.display.update()

    async def main(self):
        while True:
            # Limit FPS to 60
            time_delta = self.clock.tick(60) / 1000.0
            await asyncio.sleep(0)
            if self.state == State.RUNNING:
                self.process_inputs()
                self.update(time_delta)
                self.render()
            elif self.state is State.RESTARTING:
                self.reset()
            elif self.state is State.QUITTING:
                logging.info("Quitting.")
                return


if __name__ == "__main__":
    game = Game()
