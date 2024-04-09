"""Handles the rendering & input to the right-hand sidebar.

The sidebar contains the players score, resource queue, and the schematic library.
"""

from typing import Type

import pygame as pg

import resources
from buildings import Building
from helpers import Event, Observer, Point
from score import score
from templates import Surface
from world import RenderGrid


class Scoreboard(Surface):
    def __init__(self, width):
        self.height = 50
        self.surface = pg.Surface((width, self.height))

    def get_name(self) -> str:
        return "Scoreboard"

    def render(self) -> pg.Surface:
        self.surface.fill((255, 255, 0))
        font = pg.font.SysFont(None, 24)
        img = font.render(f"Score: {score.score}", True, (0, 0, 0))
        self.surface.blit(img, (20, 20))
        return self.surface

    def process_inputs(self):
        pass


class ResourceQueueUI(Surface, Observer):
    def __init__(self, width):
        super().__init__()
        self.height = 50
        self.surface = pg.Surface((width, self.height))
        self.resources_to_render = 5
        self.resource_queue_head: Type[resources.Resource] = resources.Resource
        self.last_resource_placed_time: int = -100000

    def event_listener(self, event: Event):
        if event == Event.PlaceResource:
            self.last_resource_placed_time = pg.time.get_ticks()

    def get_name(self) -> str:
        return "Resource Queue"

    def render(self) -> pg.Surface:
        self.surface.fill((255, 255, 255))
        distance_between_resources = 40
        resources_to_display = resources.Queue.peek_n(self.resources_to_render)
        time_delta = pg.time.get_ticks() - self.last_resource_placed_time
        animation_time = 250
        offset = 0

        if time_delta < animation_time:
            resources_to_display.insert(0, resources.Queue.last_resource_taken)
            offset = -distance_between_resources * (time_delta / animation_time)

        for i, resource in enumerate(resources_to_display):
            self.surface.blit(resource.image(), (10 + offset + (distance_between_resources * i), 10))
        return self.surface

    def update(self, _):
        pass

    def process_inputs(self, mouse_position: Point):
        pass


class SchematicBook(Surface):
    def __init__(self, width):
        self.height = 500
        self.surface = pg.Surface((width, self.height))
        self.visible_buildings = Building.BUILDING_REGISTRY

    def get_name(self) -> str:
        return "SchematicBook"

    def render(self) -> pg.Surface:
        self.surface.fill((50, 50, 50))
        height = 15
        for building in self.visible_buildings:
            font = pg.font.SysFont(None, 24)
            img = font.render(f"{building.name}", True, (0, 0, 0))
            rect = img.get_rect(center=self.surface.get_rect().center)
            self.surface.blit(img, (rect[0], height))
            height += img.get_height() + 5

            render_grid = RenderGrid(building.get_schematic(), 25)
            surf = render_grid.render(ignore_empty=True, background_color=(50, 50, 50))
            rect = surf.get_rect(center=self.surface.get_rect().center)
            self.surface.blit(surf, (rect[0], height))
            self.surface.blit(
                building.image(), (5, height + surf.get_height() // 2 - building.image().get_height() // 2)
            )
            height += surf.get_height() + 15
        return self.surface

    def process_inputs(self, mouse_position: Point):
        pass


class Sidebar(Surface):
    def __init__(self, box):
        self.box = box
        self.surface = pg.Surface(self.box.dims)
        self.surfaces = [
            Scoreboard(self.box.width),
            ResourceQueueUI(self.box.width),
            SchematicBook(self.box.width),
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
