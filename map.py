
from functools import partial
import colors
import map_primitives
import noise
import point_grid
import pygame.display
import pygame.draw
import pygame.transform
import voronoi
import random


class Map:
    def __init__(self, seed):
        print('Using seed:', seed)
        random.seed(seed)
        rand_z = random.random()
        self.noise_fn = partial(noise.pnoise3, z=rand_z, octaves=5)

    def draw(self, screen, screen_size):
        screen.fill(colors.OCEAN_BLUE)

        points = point_grid.get_fuzzy_grid(64, 64)
        faces, edges, vertices = voronoi.get_voronoi(points, primitives=map_primitives.PRIMITIVES)

        self.set_water(vertices)
        self.set_border_ocean_tiles(faces)

        for face in faces:
            pygame.draw.polygon(
                screen, face.elevation_color,
                [point.to_pygame(screen_size) for point in face.vertices]
            )
        # for ridge in ridges:
        #   pygame.draw.line(
        #       screen, DARK_GREY, ridge[0].to_pygame(MAP_SCALE), ridge[1].to_pygame(MAP_SCALE))
        # for point in points:
        #   pygame.draw.circle(screen, DARK_BLUE, point.to_pygame(MAP_SCALE), 2)

    def set_border_ocean_tiles(self, faces):
        for face in faces:
            if face.is_on_border():
                face.is_ocean = True

    def set_water(self, vertices):
        for vertex in vertices:
            vertex.set_water(self.noise_fn)

    def normalize_elevation(self, vertices):
        max_elevation = max(vertex.elevation for vertex in vertices)
        min_elevation = min(vertex.elevation for vertex in vertices)
        difference = max_elevation - min_elevation

        for vertex in vertices:
            vertex.elevation = (vertex.elevation - min_elevation) / difference
