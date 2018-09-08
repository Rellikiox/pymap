
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
import math


class Map:
    def __init__(self, seed):
        print('Using seed:', seed)
        random.seed(seed)
        base = random.randint(0, 1000)
        self.noise_fn = partial(noise.pnoise2, octaves=4, base=base)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

    def draw(self, screen, screen_size):
        screen.fill(colors.OCEAN_BLUE)

        points = point_grid.get_fuzzy_grid(64, 64)
        faces, edges, vertices = voronoi.get_voronoi(points, primitives=map_primitives.PRIMITIVES)

        self.set_water_levels(vertices)
        self.set_ocean(faces)
        self.set_elevation(vertices)
        self.add_rivers(vertices)

        for face in faces:
            pygame.draw.polygon(
                screen, face.elevation_color,
                [point.to_pygame(screen_size) for point in face.vertices]
            )

        for edge in edges:
            if edge.river_flow:
                pygame.draw.line(
                    screen, colors.RIVER_BLUE,
                    edge.vertices[0].to_pygame(screen_size),
                    edge.vertices[1].to_pygame(screen_size),
                    int(math.sqrt(edge.river_flow))
                )

    def set_water_levels(self, vertices):
        for vertex in vertices:
            vertex.set_water_chance(self.noise_fn)
            if vertex.out_of_bounds():
                vertex.is_ocean = True

    def set_ocean(self, faces):
        open_faces = set(
            [face for face in faces if any(vertex.out_of_bounds() for vertex in face.vertices)]
        )
        visited_faces = set()
        while open_faces:
            face = open_faces.pop()
            face.set_ocean(True)
            if face in visited_faces:
                continue
            for _face in face.faces:
                if _face.is_water and _face not in visited_faces:
                    _face.is_ocean = True
                    open_faces.add(_face)

            visited_faces.add(face)

    def set_elevation(self, vertices):
        max_elevation = len(vertices)
        open_set = set()
        for vertex in vertices:
            if vertex.is_ocean:
                vertex.elevation = 0
                open_set.add(vertex)
            else:
                vertex.elevation = max_elevation

        while open_set:
            vertex = open_set.pop()
            for _vertex in vertex.vertices:
                elevation = 0 if _vertex.is_ocean else vertex.elevation + 1

                if elevation < _vertex.elevation:
                    _vertex.elevation = elevation
                    open_set.add(_vertex)

        min_elevation = min(vertex.elevation for vertex in vertices)
        max_elevation = max(vertex.elevation for vertex in vertices)
        elevation_diff = max_elevation - min_elevation
        for vertex in vertices:
            vertex.elevation = (vertex.elevation - min_elevation) / elevation_diff

    def add_rivers(self, vertices):
        mountain_vertices = [vertex for vertex in vertices if vertex.elevation > 0.6]
        vertices_with_rivers = random.sample(
            mountain_vertices,
            int(math.sqrt(len(mountain_vertices))) * 2
        )

        for vertex in vertices_with_rivers:
            vertex.make_river()
