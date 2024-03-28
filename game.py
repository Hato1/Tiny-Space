import pygame

# from pygame.locals import *


class Game:
    def __init__(self):
        self._running = True
        self._display_surface = None
        self.size = self.weight, self.height = 640, 400

    def on_init(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_render(self):
        pass

    def on_loop(self):
        pass

    def on_cleanup(self):
        pygame.QUIT

    def check_inputs(self):
        """Checks for inputs from the user; mouse keys etc"""
        pass

    def on_excecute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.check_inputs()
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    game = Game()
