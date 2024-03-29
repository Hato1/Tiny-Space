"""

"""

import logging

import pygame

from buildings import Base
from helpers import GridCoordinate, Point
from resources import Queue
from templates import Surface
from tiles import Tile

common_colours = {"BLACK": (0, 0, 0), "WHITE": (200, 200, 200), "BLUE": (30, 30, 200)}


class World(Surface):
    def __init__(self):
        self.name = "World"
        self.cell_size = 50
        self.rows = 5
        self.columns = 5
        self.world_surface = pygame.Surface((self.cell_size * self.columns, self.cell_size * self.rows))
        self.mesh_colour = common_colours["BLACK"]
        self.bg_colour = common_colours["WHITE"]
        self.tiles = []
        self.initialise_tiles()

    def get_name(self) -> str:
        return self.name

    def process_inputs(self, mouse_position: Point):
        # print(mouse_position)
        grid_coordinate = self.location_to_tile(mouse_position)
        # print(grid_coordinate)
        resource = Queue.peek()
        resource_added = self.add_tile(grid_coordinate, Tile(is_empty=False, contains=resource))
        if resource_added:
            Queue.take()
        # pass

    def draw_background(self):
        max_x = self.cell_size * self.columns
        max_y = self.cell_size * self.rows
        pygame.draw.rect(self.world_surface, common_colours["BLACK"], (0, 0, max_x, max_y))

    def draw_grid_surface(self):
        max_x = self.cell_size * self.columns
        max_y = self.cell_size * self.rows
        for x in range(0, max_x, self.cell_size):
            pygame.draw.line(self.world_surface, common_colours["BLUE"], (x, 0), (x, max_y), 3)

        for y in range(0, max_y, self.cell_size):
            pygame.draw.line(self.world_surface, common_colours["BLUE"], (0, y), (max_x, y), 3)

        pygame.draw.line(self.world_surface, common_colours["BLUE"], (0, max_y), (max_x, max_y))
        pygame.draw.line(self.world_surface, common_colours["BLUE"], (max_x, 0), (max_x, max_y))

    def draw_tiles(self):
        for row in range(self.rows):
            for colum in range(self.columns):
                if self.tiles[colum][row].contains:
                    image = self.tiles[colum][row].contains.image()
                    x_loc = colum * self.cell_size
                    y_loc = row * self.cell_size
                    self.world_surface.blit(image, (x_loc, y_loc))

    def initialise_tiles(self):
        x_odd_offset = 0
        y_odd_offset = 0
        if self.columns % 2 != 0:
            x_odd_offset = 1
        if self.rows % 2 != 0:
            y_odd_offset = 1
        x_center = (self.columns + x_odd_offset) / 2 - 1
        y_center = (self.rows + y_odd_offset) / 2 - 1

        for x in range(self.columns):
            tile_row: list[Tile] = []
            for y in range(self.rows):
                if x == x_center and y == y_center:
                    tile_row.append(Tile(is_empty=False, contains=Base))
                else:
                    tile_row.append(Tile())
            self.tiles.append(tile_row)

    def render(self) -> pygame.Surface:
        self.draw_background()
        self.draw_grid_surface()
        self.draw_tiles()
        return self.world_surface

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
        if grid_loc.y < self.rows - 1:
            if self.tiles[grid_loc.x][grid_loc.y + 1].empty is False:
                return True
        # Left
        if grid_loc.x > 0:
            if self.tiles[grid_loc.x - 1][grid_loc.y].empty is False:
                return True
        # Right
        if grid_loc.x < self.columns - 1:
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
