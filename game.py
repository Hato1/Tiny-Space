"""Run this to run the game :)"""

import logging

import pygame as pg

from helpers import Box, Point
from templates import Surface
from world import World

# Box = namedtuple("Box", ["x", "y", "width", "height"])


class Game:
    def __init__(self):
        logging.info("Starting game...")
        self._running = True
        self._screen = None
        self.size = self.width, self.height = 640, 400

        # Surfaces and their position on-screen
        self.surfaces: list[tuple[Surface, Box]] = []

        pg.init()
        self._screen = pg.display.set_mode(self.size, pg.HWSURFACE | pg.DOUBLEBUF)
        self.reset()

    def reset(self):
        """Reset the game and start it again."""
        self.surfaces.append((World(), Box(0, 0, 250, 250)))
        self._running = True
        self.main_loop()

    def on_event(self, event):
        if event.type == pg.QUIT:
            self._running = False
        elif event.type == pg.KEYDOWN:
            match event.key:
                case pg.K_q:
                    self._running = False
                case pg.K_r:
                    pass
                    # game.kill_all()
                # These numbers can be used for Debug commands.
                case pg.K_1:
                    logging.info(1)
                case pg.K_2:
                    logging.info(2)
                case pg.K_3:
                    logging.info(3)
                case pg.K_4:
                    logging.info(4)
                case pg.K_5:
                    logging.info(5)
                case pg.K_6:
                    logging.info(6)
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = Point(*event.pos)
            for surface in self.surfaces:
                if surface[1].contains(mouse_position):
                    relative_position = mouse_position.relative_to(surface[1])
                    surface[0].process_inputs(relative_position)

    def process_inputs(self):
        """Checks for inputs from the user; mouse keys etc"""
        # mouse_pressed = pg.mouse.get_pressed
        # mouse_position = pg.mouse.get_pos
        for event in pg.event.get():
            self.on_event(event)

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
            assert x >= 0, f"Surface {surface[0].get_name()!r} is off the left of the screen!"
            assert y >= 0, f"Surface {surface[0].get_name()!r} is off the top of the screen!"
            assert x + width <= self.width, f"Surface {surface[0].get_name()!r} is off the right of the screen!"
            assert y + height <= self.height, f"Surface {surface[0].get_name()!r} is off the bottom of the screen!"

            self._screen.blit(surface[0].render(), (0, 0), [x, y, width, height])
        pg.display.update()

    def main_loop(self):
        while self._running:
            self.process_inputs()
            self.update()
            self.render()
        logging.info("Exiting.")


if __name__ == "__main__":
    game = Game()
