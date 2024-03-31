"""Handles the rendering & input to the right-hand sidebar.

The sidebar contains the players score, resource queue, and the schematic library.
"""

import pygame as pg

import resources
from buildings import Building
from helpers import Point
from templates import Surface
from world import RenderGrid


class Scoreboard(Surface):
    def __init__(self, width):
        self.score = 0
        self.height = 50
        self.surface = pg.Surface((width, self.height))

    def get_name(self) -> str:
        return "Scoreboard"

    def render(self) -> pg.Surface:
        self.surface.fill((255, 255, 0))
        font = pg.font.SysFont(None, 24)
        img = font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.surface.blit(img, (20, 20))
        return self.surface

    def process_inputs(self, mouse_position: Point):
        pass


class ResourceQueueUI(Surface):
    def __init__(self, width):
        self.score = 0
        self.height = 50
        self.surface = pg.Surface((width, self.height))

    def get_name(self) -> str:
        return "Scoreboard"

    def render(self) -> pg.Surface:
        self.surface.fill((255, 255, 255))
        for i, resource in enumerate(resources.Queue.peek_n(3)):
            self.surface.blit(resource.image(), (20 + (40 * i), 10))
        return self.surface

    def process_inputs(self, mouse_position: Point):
        pass


class SchematicBook(Surface):
    def __init__(self, width):
        self.height = width
        self.surface = pg.Surface((width, self.height))
        self.visible_buildings = Building.BUILDING_REGISTRY

    def get_name(self) -> str:
        return "SchematicBook"

    def render(self) -> pg.Surface:
        self.surface.fill((50, 50, 50))
        height = 15
        for building in self.visible_buildings:
            render_grid = RenderGrid(building.schematic, 25)
            surf = render_grid.render()
            rect = surf.get_rect(center=self.surface.get_rect().center)
            self.surface.blit(surf, (rect[0], height))
            height += surf.get_height() + 15
        return self.surface

    def process_inputs(self, mouse_position: Point):
        pass


class Sidebar(Surface):
    def __init__(self, width, height):
        self.surface = pg.Surface((width, height))
        self.surfaces = [
            Scoreboard(width),
            ResourceQueueUI(width),
            SchematicBook(width),
        ]

    def render(self) -> pg.Surface:
        vertical_cursor = 0
        self.surface.fill((255, 0, 0))
        for surface in self.surfaces:
            rendered = surface.render()
            self.surface.blit(rendered, (0, vertical_cursor))
            vertical_cursor += rendered.get_size()[1]
        return self.surface

    def process_inputs(self, mouse_position: Point):
        pass

    def get_name(self) -> str:
        return "Sidebar"
