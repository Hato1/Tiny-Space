"""Handles the rendering & input to the right-hand sidebar.

The sidebar contains the players score, resource queue, and the schematic library.
"""

from typing import Type

import pygame as pg

from . import resources
from .buildings import Building
from .helpers import Box, Event, Observer, Point
from .score import score
from .templates import Surface
from .world import WorldGraphicsComponent


class Scoreboard(Surface):
    def __init__(self, box: Box):
        self.box = Box(box.x, box.y, box.width, 50)
        self.height = 50
        self.surface = pg.Surface((box.width, self.height))

    def render(self) -> pg.Surface:
        self.surface.fill((255, 255, 0))
        font = pg.font.SysFont(None, 24)
        img = font.render(f"Score: {score.score}", True, (0, 0, 0))
        self.surface.blit(img, (20, 20))
        return self.surface

    def process_inputs(self, *args, **kwargs):
        pass


class ResourceQueueUI(Surface, Observer):
    def __init__(self, box):
        super().__init__()
        self.box = Box(box.x, box.y, box.width, 50)
        self.height = 50
        self.surface = pg.Surface((box.width, self.height))
        self.resources_to_render = 5
        self.resource_queue_head: Type[resources.Resource] = resources.Resource
        self.last_resource_placed_time: int = -100000

    def event_listener(self, event: Event):
        if event == Event.PlaceResource:
            self.last_resource_placed_time = pg.time.get_ticks()

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

    def update(self):
        pass

    def process_inputs(self, mouse_position: Point):
        pass


class SchematicBook(Surface):
    def __init__(self, box: Box):
        self.box = Box(box.x, box.y, box.width, 500)
        self.height = 500
        self.surface = pg.Surface((box.width, self.height))
        self.visible_buildings = Building.BUILDING_REGISTRY

    def render(self) -> pg.Surface:
        self.surface.fill((50, 50, 50))
        height = 15
        for building in self.visible_buildings:
            font = pg.font.SysFont(None, 24)
            img = font.render(f"{building.name}", True, (0, 0, 0))
            rect = img.get_rect(center=self.surface.get_rect().center)
            self.surface.blit(img, (rect[0], height))
            height += img.get_height() + 5

            schematic_renderer = WorldGraphicsComponent(building.get_schematic().size, 25)
            schematic_renderer.draw_cursor = lambda grid: None  # type: ignore[method-assign]
            schematic_renderer.draw_build_hammers = lambda: True  # type: ignore[method-assign]
            schematic_renderer.box = Box(
                self.box.x + schematic_renderer.surface.get_rect(center=self.surface.get_rect().center)[0],
                self.box.y + height,
                schematic_renderer.box.width,
                schematic_renderer.box.height,
            )
            surf = schematic_renderer.render(building.get_schematic(), ignore_empty=True, background_color=(50, 50, 50))
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

        subbox = [self.box.x, self.box.y, self.box.width, self.box.height]
        self.surfaces: list[Surface] = []
        surface_types: list[Type[Surface]] = [
            Scoreboard,
            ResourceQueueUI,
            SchematicBook,
        ]
        for surface in surface_types:
            self.surfaces.append(surface(Box(*subbox)))  # type: ignore[call-arg]
            subbox[1] += self.surfaces[-1].box.height

    def render(self) -> pg.Surface:
        vertical_cursor = 0
        self.surface.fill((255, 0, 0))
        for surface in self.surfaces:
            surface.box = Box(self.box.x, self.box.y + vertical_cursor, surface.box.width, self.box.height)
            rendered = surface.render()
            relative_box = Box(*(surface.box.top_left - self.box.top_left), *self.box.dims)
            self.surface.blit(rendered, relative_box)
            vertical_cursor += rendered.get_size()[1]
        return self.surface

    def process_inputs(self, mouse_position: Point):
        pass
