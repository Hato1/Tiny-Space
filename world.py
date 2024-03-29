"""

"""

import pygame
import tiles

from templates import Surface

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
        self.set_grid_surface()
        self.generate_tiles()

    def get_name(self) -> str:
        return self.name

    def set_grid_surface(self):
        max_x = self.cell_size * self.columns
        max_y = self.cell_size * self.rows
        for x in range(0, max_x, self.cell_size):
            pygame.draw.line(self.world_surface, common_colours["BLUE"], (x, 0), (x, max_y), 3)

        for y in range(0, max_y, self.cell_size):
            pygame.draw.line(self.world_surface, common_colours["BLUE"], (0, y), (max_x, y), 3)
            
        pygame.draw.line(self.world_surface, common_colours['BLUE'],
                         (0, max_y), (max_x, max_y))
        pygame.draw.line(self.world_surface, common_colours['BLUE'],
                         (max_x, 0), (max_x, max_y))
        
    def generate_tiles(self):
        x_odd_offset = 0
        y_odd_offset = 0
        if self.columns % 2 != 0:
            x_odd_offset = 1
        if self.rows % 2 != 0:
            y_odd_offset = 1
        x_center = (self.columns + x_odd_offset)/2 - 1
        y_center = (self.rows + y_odd_offset)/2 - 1
        
        for x in range(self.columns):
            tile_row = []
            for y in range(self.rows):
                if (x == x_center and y == y_center):
                    tile_row.append(tiles.Base)
                else:
                    tile_row.append(tiles.EmptyTile)
            self.tiles.append(tile_row)
            
        for i in self.tiles:
            print(i)

    def render(self) -> pygame.Surface:
        return self.world_surface
