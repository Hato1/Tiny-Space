"""

"""

import logging
from typing import Type

import pygame

from buildings import Base, Building
from helpers import GridCoordinate, Point
from resources import Queue, Resource
from templates import Surface
from tiles import Tile

common_colours = {"BLACK": (0, 0, 0), "WHITE": (200, 200, 200), "BLUE": (30, 30, 200)}


class World(Surface):
    def __init__(self, width: int, height: int, grid_size=(7, 5)):
        self.name = "World"
        self.cell_size = 50
        self.grid_size = Point(*grid_size)
        # Add an extra two pixels of padding to fit the lined border.
        # TODO: Draw the border on the outer canvas instead of on the grid.
        self.grid_pixel_size = Point(self.grid_size.x * self.cell_size + 2, self.grid_size.y * self.cell_size + 2)
        self.canvas_size = Point(width, height)

        assert self.grid_size.x * self.cell_size < width, "Grid too wide for display area!"
        assert self.grid_size.y * self.cell_size < height, "Grid too tall for display area!"
        self.grid_surface = pygame.Surface(self.grid_pixel_size)
        self.world_surface = pygame.Surface(self.canvas_size)
        self.mesh_colour = common_colours["BLACK"]
        self.bg_colour = common_colours["WHITE"]
        self.tiles: list[list[Tile]] = []
        self.initialise_tiles()

    def get_name(self) -> str:
        return self.name

    def process_inputs(self, mouse_position: Point):
        mouse_position = Point(mouse_position.x - self.grid_coords().x, mouse_position.y - self.grid_coords().y)
        grid_coordinate = self.location_to_tile(mouse_position)
        # Fails if clicked elsewhere on the canvas.
        if self.valid_grid_coordinate(grid_coordinate):
            resource = Queue.peek()
            resource_added = self.add_tile(grid_coordinate, Tile(is_empty=False, contains=resource))
            if resource_added:
                Queue.take()
        # pass

    def draw_grid_surface(self):
        """Draw the grid lines in the center of the display."""
        line_width = 2
        min_x = 0
        min_y = 0
        max_x, max_y = self.grid_pixel_size
        for x in range(min_x, max_x, self.cell_size):
            pygame.draw.line(self.grid_surface, common_colours["BLUE"], (x, min_y), (x, max_y), line_width)

        for y in range(min_y, max_y, self.cell_size):
            pygame.draw.line(self.grid_surface, common_colours["BLUE"], (min_x, y), (max_x, y), line_width)

        pygame.draw.line(self.grid_surface, common_colours["BLUE"], (min_x, max_y), (max_x, max_y), line_width)
        pygame.draw.line(self.grid_surface, common_colours["BLUE"], (max_x, min_y), (max_x, max_y), line_width)

    def draw_tile(self, thing: Type[Resource] | Type[Building], x, y):
        asset_size = Point(*thing.image().get_size())
        # half_asset_size = asset_size[0] // 2, asset_size[1] // 2
        self.grid_surface.blit(
            thing.image(),
            (
                (x + 0.5) * self.cell_size - asset_size.x // 2,
                (y + 0.5) * self.cell_size - asset_size.y // 2,
            ),
        )

    def draw_tiles(self):
        for x in range(self.grid_size.x):
            for y in range(self.grid_size.y):
                if thing := self.tiles[x][y].contains:
                    self.draw_tile(thing, x, y)

    def grid_coords(self) -> Point:
        """Where to blit the grid onto the canvas."""
        return Point(
            self.canvas_size.x // 2 - self.grid_pixel_size.x // 2, self.canvas_size.y // 2 - self.grid_pixel_size.y // 2
        )

    def render(self) -> pygame.Surface:
        self.world_surface.fill(common_colours["BLACK"])
        # self.grid_surface
        self.draw_grid_surface()
        self.draw_tiles()
        self.world_surface.blit(self.grid_surface, self.grid_coords())
        return self.world_surface

    def initialise_tiles(self):
        self.tiles = [[Tile() for _ in range(self.grid_size.y)] for _ in range(self.grid_size.x)]
        self.tiles[self.grid_size.x // 2][self.grid_size.y // 2] = Tile(is_empty=False, contains=Base)

    def location_to_tile(self, location: Point) -> GridCoordinate:
        return GridCoordinate(int(location.x / self.cell_size), int(location.y / self.cell_size))

    def change_tile(self, grid_loc: GridCoordinate, tile):
        self.tiles[grid_loc.x][grid_loc.y] = tile

    def check_for_adjacencies(self, grid_loc: GridCoordinate):
        # Up
        if grid_loc.y > 0:
            if self.tiles[grid_loc.x][grid_loc.y - 1].empty is False:
                return True
        # Down
        if grid_loc.y < self.grid_size.y - 1:
            if self.tiles[grid_loc.x][grid_loc.y + 1].empty is False:
                return True
        # Left
        if grid_loc.x > 0:
            if self.tiles[grid_loc.x - 1][grid_loc.y].empty is False:
                return True
        # Right
        if grid_loc.x < self.grid_size.x - 1:
            if self.tiles[grid_loc.x + 1][grid_loc.y].empty is False:
                return True
        return False

    def add_tile(self, grid_loc: GridCoordinate, tile: Tile):
        if self.tiles[grid_loc.x][grid_loc.y].empty is False:
            logging.warning("Space Occupied at {},{}".format(grid_loc.x, grid_loc.y))
            return False
        if self.check_for_adjacencies(grid_loc) is False:
            logging.warning("Space not adjacent to existing block at {},{}".format(grid_loc.x, grid_loc.y))
            return False
        self.change_tile(grid_loc, tile)
        return True

    def valid_grid_coordinate(self, grid_coordinate: GridCoordinate):
        if grid_coordinate.x < 0 or grid_coordinate.y < 0:
            return False
        if grid_coordinate.x >= self.grid_size.x or grid_coordinate.y >= self.grid_size.y:
            return False
        return True
