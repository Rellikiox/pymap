
from operator import attrgetter
from functools import partial
import colors
import map_primitives
import noise
import point_grid
import pygame.display
import pygame.font
import pygame.draw
import pygame.gfxdraw
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
        self.font = pygame.font.SysFont('Comic Sans MS', 12)

    def draw(self, screen, screen_size):
        screen.fill(colors.OCEAN_BLUE)

        points = point_grid.get_fuzzy_grid(32, 32)
        faces, edges, vertices = voronoi.get_voronoi(points, primitives=map_primitives.PRIMITIVES)

        self.set_water_levels(vertices)
        self.reset_orphaned_water_vertices(vertices)
        self.set_ocean(faces)
        self.set_elevation(vertices)
        self.redistribute_elevation(vertices)
        self.add_rivers(vertices)
        self.set_moisture(vertices)
        self.redistribute_moisture(vertices)

        for face in faces:
            draw_filled_aa_polygon(
                screen,
                [point.scaled(screen_size).tuple() for point in face.vertices],
                face.elevation_color
            )

        for edge in edges:
            if edge.river_flow:
                draw_filled_aa_polygon(
                    screen,
                    edge.as_rectangle(math.sqrt(edge.river_flow), screen_size),
                    colors.RIVER_BLUE
                )

        # for vertex in vertices:
        #     if vertex.is_lake:
        #         screen.blit(
        #             self.font.render(str(round(vertex.elevation, 2)), False, colors.WHITE),
        #             vertex.to_pygame(screen_size)
        #         )

        # print(len([vertex.elevation for vertex in vertices if vertex.is_lake]))

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

    def reset_orphaned_water_vertices(self, vertices):
        for vertex in vertices:
            if vertex.is_water:
                vertex.is_water = any(face.is_water for face in vertex.faces)

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
                if vertex.is_lake and _vertex.is_lake:
                    elevation = vertex.elevation
                else:
                    elevation = vertex.elevation + 1

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
            int(math.sqrt(len(mountain_vertices)) * 1.5)
        )

        for vertex in vertices_with_rivers:
            vertex.make_river()

    def redistribute_elevation(self, vertices):
        land_vertices = [vertex for vertex in vertices if not vertex.is_water]
        sorted_by_elevation = sorted(land_vertices, key=attrgetter('elevation'))
        scale = 1.1

        for idx, vertex in enumerate(sorted_by_elevation):
            relative_position = idx / (len(sorted_by_elevation) - 1)
            vertex.elevation = math.sqrt(scale) - math.sqrt(scale * (1 - relative_position))

    def set_moisture(self, vertices):
        moist_vertices = set()
        for vertex in vertices:
            if vertex.is_lake or vertex.river_flow:
                vertex.moisture = min(3, vertex.river_flow * 0.2) if vertex.river_flow else 1
                moist_vertices.add(vertex)
            else:
                vertex.moisture = 0

        while moist_vertices:
            vertex = moist_vertices.pop()
            for _vertex in vertex.vertices:
                new_moisture = vertex.moisture * 0.85
                if new_moisture > _vertex.moisture:
                    _vertex.moisture = new_moisture
                    moist_vertices.add(_vertex)

        for vertex in vertices:
            if vertex.is_ocean or vertex.is_coast:
                vertex.moisture = 1

    def redistribute_moisture(self, vertices):
        sorted_by_moisture = sorted(vertices, key=attrgetter('moisture'))

        for idx, vertex in enumerate(sorted_by_moisture):
            vertex.moisture = idx / (len(sorted_by_moisture) - 1)


def draw_filled_aa_polygon(screen, points, color):
    pygame.gfxdraw.aapolygon(screen, points, color)
    pygame.gfxdraw.filled_polygon(screen, points, color)
