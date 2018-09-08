
from functools import partial
import colors
import map_primitives
import noise
import point_grid
import pygame.display
import pygame.font
import pygame.draw
import pygame.transform
import voronoi
import random


class Map:
    def __init__(self, seed):
        print('Using seed:', seed)
        random.seed(seed)
        rand_z = random.random()

        self.noise_fn = partial(noise.pnoise3, z=rand_z, octaves=8, lacunarity=8, repeatx=8, repeaty=8)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

    def draw(self, screen, screen_size):
        screen.fill(colors.OCEAN_BLUE)

        points = point_grid.get_fuzzy_grid(64, 64)
        faces, edges, vertices = voronoi.get_voronoi(points, primitives=map_primitives.PRIMITIVES)

        self.set_water(vertices)

        base = random.randint(0, 1000)
        for vertex in vertices:
            vertex.set_new_factor(base)
        # self.normalize_new_factor(vertices)

        for idx, face in enumerate(faces):
            color = colors.greyscale(sum(vertex.new_factor for vertex in face.vertices) / len(face.vertices))
            color = face.elevation_color
            pygame.draw.polygon(
                screen, color,
                [point.to_pygame(screen_size) for point in face.vertices]
            )

    def set_water(self, vertices):
        for vertex in vertices:
            vertex.set_water(self.noise_fn)

    def normalize_new_factor(self, vertices):
        max_new_factor = max(vertex.new_factor for vertex in vertices)
        min_new_factor = min(vertex.new_factor for vertex in vertices)
        difference = max_new_factor - min_new_factor

        for vertex in vertices:
            vertex.new_factor = (vertex.new_factor - min_new_factor) / difference
