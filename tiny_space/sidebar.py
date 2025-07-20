"""Handles the rendering & input to the right-hand sidebar.

The sidebar contains the players score, resource queue, and the schematic library.
"""

from typing import Type

import pygame as pg

from . import resources
from .buildings import Building
from .helpers import Event, Observer, Point
from .score import score
from .templates import GraphicsComponent
from .world import Color, WorldGraphicsComponent


class Scoreboard(GraphicsComponent):
    def __init__(self, dims: Point):
        self.surface = pg.Surface(dims)

    def render(self) -> pg.Surface:
        self.surface.fill(pg.Color("yellow"))
        font = pg.font.SysFont(None, 24)
        img = font.render(f"Score: {score.score}", True, pg.Color("black"))
        self.surface.blit(img, (20, 20))
        return self.surface

    def process_inputs(self, *args, **kwargs):
        pass


class ResourceQueueUI(GraphicsComponent, Observer):
    distance_between_resources = 40
    resources_to_render = 5
    animation_duration = 250

    def __init__(self, dims: Point):
        super().__init__()
        self.surface = pg.Surface(dims)
        self.resource_queue_head: Type[resources.Resource] = resources.Resource
        self.last_resource_placed_time: int = -100000

    def event_listener(self, event: Event):
        if event == Event.PlaceResource:
            self.last_resource_placed_time = pg.time.get_ticks()

    def render(self) -> pg.Surface:
        self.surface.fill(pg.Color("white"))
        resources_to_display = resources.Queue.peek_n(self.resources_to_render)
        time_delta = pg.time.get_ticks() - self.last_resource_placed_time
        offset = 0

        if time_delta < self.animation_duration:
            resources_to_display.insert(0, resources.Queue.last_resource_taken)
            offset = int(-self.distance_between_resources * (time_delta / self.animation_duration))

        for i, resource in enumerate(resources_to_display):
            self.surface.blit(resource.image(), (10 + offset + (self.distance_between_resources * i), 10))
        return self.surface

    def process_inputs(self, mouse_position: Point):
        pass


class SchematicBook(GraphicsComponent):
    def __init__(self, dims: Point):
        self.surface = pg.Surface(dims)
        self.constructable_buildings = [b for b in Building.BUILDING_REGISTRY if b.is_buildable()]

    def render(self) -> pg.Surface:
        self.surface.fill((50, 50, 50))
        height = 15
        for building in self.constructable_buildings:
            font = pg.font.SysFont(None, 24)
            img = font.render(f"{building.get_name()}", True, pg.Color("black"))
            rect = img.get_rect(center=self.surface.get_rect().center)
            self.surface.blit(img, (rect[0], height))
            height += img.get_height() + 5

            schematic_renderer = WorldGraphicsComponent(building.get_schematic().size, 25)
            schematic_renderer.draw_cursor = lambda grid, mouse_pos: None  # type: ignore[method-assign]
            schematic_renderer.draw_build_hammers = lambda: True  # type: ignore[method-assign]
            surf = schematic_renderer.render(
                building.get_schematic(), mouse_pos=Point(-1, -1), ignore_empty=True, background_color=Color.DARK_GREY
            )
            rect = surf.get_rect(center=self.surface.get_rect().center)
            self.surface.blit(surf, (rect[0], height))
            self.surface.blit(
                building.image(), (5, height + surf.get_height() // 2 - building.image().get_height() // 2)
            )
            height += surf.get_height() + 15
        return self.surface

    def process_inputs(self, mouse_position: Point):
        pass


class SchematicEntry(GraphicsComponent):
    font_size = 24

    def __init__(self, dims: Point, building: type[Building]):
        self.surface = pg.Surface(dims)
        self.building = building
        self.font = pg.font.SysFont(None, self.font_size)

    def render(self, *args, **kwargs):
        self.surface.fill((50, 50, 50))

        # Draw building name.
        title = self.font.render(f"{self.building.get_name()}", True, pg.Color("black"))
        rect = title.get_rect(midtop=self.surface.get_rect().midtop)
        self.surface.blit(title, rect)

        # Draw building schematic.
        schematic_renderer = WorldGraphicsComponent(self.building.get_schematic().size, 25)
        schematic_renderer.draw_cursor = lambda grid, mouse_pos: None  # type: ignore[method-assign]
        schematic_renderer.draw_build_hammers = lambda: True  # type: ignore[method-assign]
        surf = schematic_renderer.render(
            self.building.get_schematic(), mouse_pos=Point(-1, -1), ignore_empty=True, background_color=Color.DARK_GREY
        )
        rect = surf.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(surf, rect)

        # Draw building icon.
        rect = self.building.image().get_rect(midleft=(5, rect.centery))
        self.surface.blit(self.building.image(), rect)
        return self.surface


class SchematicBook2(GraphicsComponent):
    def __init__(self, dims: Point):
        self.surface = pg.Surface(dims)
        self.constructable_buildings = [b for b in Building.BUILDING_REGISTRY if b.is_buildable()]
        self.building_entries = {
            b: SchematicEntry(Point(dims.x, dims.y // 3), b) for b in Building.BUILDING_REGISTRY if b.is_buildable()
        }

    def render(self, *args, **kwargs):
        for i, schematic_entry in enumerate(self.building_entries.values()):
            self.surface.blit(schematic_entry.render(), (0, self.surface.height * (i / 3)))
        return self.surface

    def process_inputs(self, mouse_position: Point):
        pass


class Sidebar(GraphicsComponent):
    def __init__(self, dims: Point):
        self.surface = pg.Surface(dims)

        scoreboard_height = 50
        resource_queue_height = 50
        schematic_book_height = self.surface.height - scoreboard_height - resource_queue_height

        self.surfaces: list[GraphicsComponent] = [
            Scoreboard(Point(dims.x, scoreboard_height)),
            ResourceQueueUI(Point(dims.x, resource_queue_height)),
            # SchematicBook(Point(dims.x, 500)),
            SchematicBook2(Point(dims.x, schematic_book_height)),
        ]

    def render(self, *args, **kwargs) -> pg.Surface:
        self.surface.fill((255, 0, 0))
        vertical_cursor = 0
        for surface in self.surfaces:
            rendered = surface.render()
            self.surface.blit(rendered, (0, vertical_cursor))
            vertical_cursor += rendered.get_size()[1]
        return self.surface

    def process_inputs(self, mouse_position: Point):
        pass

    def update(self, time_delta):
        for surf in self.surfaces:
            surf.update(time_delta)
