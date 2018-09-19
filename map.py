
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
    def __init__(self, width, seed):
        self.width = width
        print('Using seed:', seed)
        random.seed(seed)
        base = random.randint(0, 1000)
        self.noise_fn = partial(noise.pnoise2, octaves=4, base=base)

    def create(self):
        points = point_grid.get_fuzzy_grid(self.width, self.width)
        faces, edges, vertices = voronoi.get_voronoi(points, primitives=map_primitives.PRIMITIVES)

        self.set_water_levels(vertices)
        self.reset_orphaned_water_vertices(vertices)
        self.set_ocean(faces)
        self.set_elevation(vertices)
        self.redistribute_elevation(vertices)
        self.add_rivers(vertices)
        self.set_moisture(vertices)
        self.redistribute_moisture(vertices)

        self.faces = faces
        self.edges = edges
        self.vertices = vertices

    def draw(self, screen, screen_size, font, draw_mode='map'):
        if draw_mode == 'noise':
            pixels = {}
            base = random.randint(0, screen_size)
            scale = 3 / screen_size
            for y in range(screen_size):
                for x in range(screen_size):

                    # pixels[(x, y)] = noise.pnoise2(x * scale, y * scale, base=base, octaves=4)
                    pixels[(x, y)] = noise.pnoise2(x * scale, y * scale, base=base)
                    pixels[(x, y)] += 0.5 * noise.pnoise2(x * scale * 2, y * scale * 2, base=base)
                    pixels[(x, y)] += 0.25 * noise.pnoise2(x * scale * 4, y * scale * 4, base=base)
                    pixels[(x, y)] += 0.125 * noise.pnoise2(x * scale * 8, y * scale * 8, base=base)

            max_pixel = max(value for value in pixels.values())
            min_pixel = min(value for value in pixels.values())
            print(min_pixel, max_pixel)
            pixel_diff = max_pixel - min_pixel

            for pixel, pixel_value in pixels.items():
                pixel_value = ((pixel_value - min_pixel) / pixel_diff)
                if pixel_value < 0.34:
                    color = (pixel_value * 255, 0, 0)
                elif pixel_value < 0.67:
                    color = (0, pixel_value * 255, 0)
                else:
                    color = (0, 0, pixel_value * 255)

                screen.set_at(pixel, color)
                # screen.set_at(pixel, colors.greyscale(pixel_value + 0.5))
            return

        for face in self.faces:
            draw_filled_aa_polygon(
                screen,
                [point.scaled(screen_size).tuple() for point in face.vertices],
                face.elevation_color
            )

        # for edge in self.edges:
        #     if not edge.is_ocean and not edge.river_flow and not edge.is_boundary:
        #         draw_filled_aa_polygon(
        #             screen,
        #             edge.as_rectangle(0.25, screen_size),
        #             edge.inner_boundary_color
        #         )

        for edge in self.edges:
            if not edge.is_ocean and not edge.river_flow and edge.is_boundary:
                draw_filled_aa_polygon(
                    screen,
                    edge.as_rectangle(2, screen_size),
                    edge.outter_boundary_color
                )

        for edge in self.edges:
            if edge.river_flow:
                draw_filled_aa_polygon(
                    screen,
                    edge.as_rectangle(min(3, math.sqrt(edge.river_flow)), screen_size),
                    colors.RIVER_BLUE
                )

        # for vertex in self.vertices:
        #     if vertex.is_lake:
        #         screen.blit(
        #             font.render(str(round(vertex.elevation, 2)), False, colors.WHITE),
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

    def to_dict(self):
        return {
            'points': {
                id(vertex): vertex.to_dict()
                for vertex in self.vertices
            }
        }


def draw_filled_aa_polygon(screen, points, color):
    pygame.gfxdraw.aapolygon(screen, points, color)
    pygame.gfxdraw.filled_polygon(screen, points, color)
