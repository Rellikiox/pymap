
import datetime
import os

import delaunay
import grid
import pygame.display
import pygame.draw
import pygame.transform


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 128)
DARK_GREEN = (0, 64, 0)
DARKISH_GREEN = (0, 128, 0)
DARK_GREY = (128, 128, 128)
OCEAN_BLUE = (175, 214, 254)
GRASS_GREEN = (189, 237, 174)
MOUNTAIN_BROWN = (58, 48, 40)
MAP_SCALE = 900


class Map:

    def draw(self, screen):
        points = grid.get_fuzzy_grid(64, 64)
        regions, ridges = delaunay.voronoi(points)
        cells = [Cell(region) for region in regions]

        for cell in cells:
            pygame.draw.polygon(
                screen, cell.color(),
                [point.to_pygame(MAP_SCALE) for point in cell.region.points]
            )
        # for ridge in ridges:
        #   pygame.draw.line(
        #       screen, DARK_GREY, ridge[0].to_pygame(MAP_SCALE), ridge[1].to_pygame(MAP_SCALE))
        # for point in points:
        #   pygame.draw.circle(screen, DARK_BLUE, point.to_pygame(MAP_SCALE), 2)


def color_in_range(start_color, end_color, percentage):
    return tuple(
        [int(start + (end - start) * percentage) for start, end in zip(start_color, end_color)]
    )


class Cell:
    def __init__(self, region):
        self.region = region
        self.centre = region.centre()

    def color(self):
        if any(point.out_of_bounds() for point in self.region.points):
            return OCEAN_BLUE

        color = color_in_range(WHITE, BLACK, self.centre.distance_to_map_centre_normalized())
        return color
