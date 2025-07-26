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

    def render(self, **kwargs) -> pg.Surface:
        self.surface.fill(pg.Color("yellow"))
        font = pg.font.SysFont(None, 24)
        img = font.render(f"Score: {score.score}", True, pg.Color("black"))
        self.surface.blit(img, (20, 20))
        return self.surface


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

    def render(self, **kwargs) -> pg.Surface:
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


class SchematicEntry(GraphicsComponent):
    font_size = 18
    font_file = "assets/Orbitron-Regular.ttf"

    def __init__(self, dims: Point, building: type[Building]):
        self.surface = pg.Surface(dims)
        self.building = building
        self.font = pg.font.Font(self.font_file, size=self.font_size)

    def render(self, **kwargs):
        self.surface.fill(Color.DARK_GREY)
        gap_between_elements = 5

        sr = self.surface.get_rect()

        # Draw building name.
        title = self.font.render(f"{self.building.get_name()}", True, pg.Color("black"))
        name_rect = title.get_rect(midtop=self.surface.get_rect().midtop)
        name_rect.y += gap_between_elements
        self.surface.blit(title, name_rect)

        # Draw description box.
        description_rect = pg.Rect()
        description_rect.size = (sr.width * 9 // 10, sr.height // 4)
        description_rect.midtop = (sr.centerx, name_rect.bottom + gap_between_elements)
        pg.draw.rect(self.surface, (100, 100, 100), description_rect, border_radius=10)
        pg.draw.rect(self.surface, (20, 20, 20), description_rect, width=3, border_radius=10)

        # Draw building icon.
        rect = self.building.image().get_rect(
            midleft=(description_rect.left + gap_between_elements, description_rect.centery)
        )
        self.surface.blit(self.building.image(), rect)

        # Draw building effect.
        # TODO

        # Draw build button.
        build_rect = pg.Rect()
        build_rect.size = (sr.width * 6 // 10, sr.height // 10)
        build_rect.midbottom = (sr.centerx, sr.bottom - gap_between_elements)
        pg.draw.rect(self.surface, (255, 92, 0), build_rect, border_radius=10)
        pg.draw.rect(self.surface, (128, 46, 0), build_rect, width=3, border_radius=10)
        build_text = self.font.render("Build", True, pg.Color("black"))
        build_text_rect = build_text.get_rect(center=build_rect.center)
        self.surface.blit(build_text, build_text_rect)

        # Draw building schematic.
        schematic_renderer = WorldGraphicsComponent(self.building.get_schematic().size, 35, schematic=True)
        surf = schematic_renderer.render(self.building.get_schematic(), background_color=Color.DARK_GREY)
        y = description_rect.bottom + ((build_rect.top - description_rect.bottom) // 2)
        rect = surf.get_rect(center=(sr.centerx, y))
        self.surface.blit(surf, rect)

        return self.surface


class SchematicBook(GraphicsComponent):
    font_size = 12
    font_file = "assets/Orbitron-Regular.ttf"

    # Button grid
    entries_per_row = 6
    button_height = 20
    button_bar_height = 20 * 2

    def __init__(self, dims: Point):
        self.surface = pg.Surface(dims)
        self.building_entries = {
            b: SchematicEntry(Point(dims.x, (dims.y - self.button_bar_height)), b)
            for b in Building.BUILDING_REGISTRY
            if b.is_buildable()
        }
        self.selected_building = list(self.building_entries.keys())[0]
        self.font = pg.font.Font(self.font_file, size=self.font_size)

    def render_button(self, rect: pg.Rect, color: tuple[int, int, int] | None, text: str):
        """Render a single button from the button bar."""
        border_color = (30, 30, 200)

        if color:
            pg.draw.rect(self.surface, color, rect, border_radius=5)
        pg.draw.rect(self.surface, border_color, rect, width=2, border_radius=5)

        # Number
        number = self.font.render(text, True, pg.Color("white"))
        name_rect = number.get_rect(center=rect.center)
        self.surface.blit(number, name_rect)

    def render_button_bar(self, mouse_position: Point):
        for i, building in enumerate(self.building_entries.keys()):
            x = (i % self.entries_per_row) * self.surface.width / self.entries_per_row
            y = (i // self.entries_per_row) * self.button_height
            rect = pg.Rect(x, y, self.surface.width / self.entries_per_row, self.button_height)
            color = None
            if building is self.selected_building:
                color = (83, 109, 254)
            elif building is self.get_moused_building(mouse_position):
                color = (123, 159, 254)
            else:
                color = None
            self.render_button(rect, color, str(i + 1))

    def render(self, *, mouse_position: Point, **kwargs):
        self.surface.fill(pg.Color("black"))
        self.render_button_bar(mouse_position)

        building = self.get_moused_building(mouse_position) or self.selected_building
        surf = self.building_entries[building].render()
        self.surface.blit(surf, (0, self.button_bar_height))
        return self.surface

    def get_moused_building(self, mouse_position: Point) -> type[Building] | None:
        """Get the building for the button-grid button at coordinate."""
        if self.surface.get_rect().collidepoint(mouse_position):
            x = mouse_position.x // (self.surface.width // self.entries_per_row)
            y = mouse_position.y // self.button_height
            index = y * 6 + x
            if index < len(self.building_entries):
                return list(self.building_entries)[index]
        return None

    def process_inputs(self, mouse_position: Point):
        if moused_building := self.get_moused_building(mouse_position):
            self.selected_building = moused_building


class Sidebar(GraphicsComponent):
    def __init__(self, dims: Point):
        self.surface = pg.Surface(dims)

        scoreboard_height = dims.y // 8
        resource_queue_height = dims.y // 8
        schematic_book_height = self.surface.height - scoreboard_height - resource_queue_height

        self.surfaces: list[tuple[Point, GraphicsComponent]] = [
            (Point(0, 0), Scoreboard(Point(dims.x, scoreboard_height))),
            (Point(0, scoreboard_height), ResourceQueueUI(Point(dims.x, resource_queue_height))),
            (Point(0, scoreboard_height + resource_queue_height), SchematicBook(Point(dims.x, schematic_book_height))),
        ]

    def render(self, mouse_position: Point, *args, **kwargs) -> pg.Surface:
        self.surface.fill((255, 0, 0))
        vertical_cursor = 0
        for _pos, surface in self.surfaces:
            rendered = surface.render(mouse_position=mouse_position - _pos)
            self.surface.blit(rendered, (0, vertical_cursor))
            vertical_cursor += rendered.get_size()[1]
        return self.surface

    def process_inputs(self, mouse_position: Point):
        self.process_inputs_subsurfaces(mouse_position, self.surfaces)

    def update(self, time_delta):
        for _pos, surf in self.surfaces:
            surf.update(time_delta)
