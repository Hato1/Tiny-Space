'''

'''
import pygame

common_colours = {'BLACK': (0, 0, 0),
                  'WHITE': (200, 200, 200),
                  'BLUE': (30, 30, 200)}

class World:
    def __init__(self):
        self.name = "World"
        self.cell_size = 500
        self.rows = 5
        self.columns = 5
        self.world_surface = pygame.Surface((self.cell_size*self.columns, self.cell_size*self.rows))
        self.mesh_colour = common_colours['BLACK']
        self.bg_colour = common_colours['WHITE']
        self.set_grid_surface()
        
    def set_grid_surface(self):
        max_x = self.cell_size * self.columns
        max_y = self.cell_size * self.rows
        # pygame.draw.line(self.world_surface, common_colours['BLUE'], 
        #                  (0, 0), (0, max_y))
        # pygame.draw.line(self.world_surface, common_colours['BLUE'], 
        #                  (0, 0), (max_x, 0))
        for x in range(0, self.columns):
            print(x)
            pygame.draw.line(self.world_surface, common_colours['BLUE'], (x, 0), (x, max_y), 3)
            
        for y in range(0, self.rows):
            pygame.draw.line(self.world_surface, common_colours['BLUE'], (0, y), (max_x, y), 3)
    
    def render(self) -> pygame.Surface:
        return self.world_surface
    
