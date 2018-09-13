
from operator import attrgetter
from grid import Face, Edge, Vertex
import colors
import math


class MapFace(Face):
    is_ocean = False

    def color(self):
        if any(vertex.out_of_bounds() for vertex in self.vertices):
            return colors.OCEAN_BLUE

        return colors.color_in_range(
            colors.WHITE, colors.BLACK, self.centre.distance_to_map_centre()
        )

    @property
    def elevation_color(self):
        if self.is_ocean:
            return colors.DEEP_BLUE
        if self.is_water:
            return colors.RIVER_BLUE
        if self.is_coast:
            return colors.SAND
        return self.biome.color

    @property
    def centre(self):
        return sum(self.vertices) / len(self.vertices)

    @property
    def is_water(self):
        return len([vertex for vertex in self.vertices if not vertex.is_water]) < 1

    @property
    def is_lake(self):
        return self.is_water and not self.is_ocean

    @property
    def is_coast(self):
        return len([vertex for vertex in self.vertices if vertex.is_coast]) > len(self.vertices) * 0.7

    @property
    def moisture(self):
        return sum(vertex.moisture for vertex in self.vertices) / len(self.vertices)

    @property
    def elevation(self):
        return sum(vertex.elevation for vertex in self.vertices) / len(self.vertices)

    @property
    def biome(self):
        return Biome(self)

    def is_on_border(self):
        return any(vertex.out_of_bounds() for vertex in self.vertices)

    def set_ocean(self, is_ocean):
        self.is_ocean = is_ocean
        for vertex in self.vertices:
            vertex.is_ocean = True


class MapEdge(Edge):
    river_flow = 0

    @property
    def is_ocean(self):
        return all(vertex.is_ocean for vertex in self.vertices)

    @property
    def is_boundary(self):
        if len(self.faces) == 1:
            return False
        return self.faces[0].biome.biome_type != self.faces[1].biome.biome_type

    @property
    def outter_boundary_color(self):
        dominant_color = sorted(
            self.faces, key=attrgetter('elevation'), reverse=True
        )[0].biome.color
        return colors.color_in_range(dominant_color, colors.BLACK, 0.25)

    @property
    def inner_boundary_color(self):
        return colors.color_in_range(self.faces[0].biome.color, colors.WHITE, 0.25)

    def as_rectangle(self, width, scale):
        p0 = self.vertices[0] * scale
        p1 = self.vertices[1] * scale

        dx = p1.x - p0.x
        dy = p1.y - p0.y
        line_length = math.sqrt(dx * dx + dy * dy)
        dx /= line_length
        dy /= line_length
        px = 0.5 * width * (-dy)
        py = 0.5 * width * dx

        return [
            (p0.x + px, p0.y + py),
            (p1.x + px, p1.y + py),
            (p1.x - px, p1.y - py),
            (p0.x - px, p0.y - py)
        ]


class MapVertex(Vertex):
    elevation = None
    moisture = 0
    river_flow = 0
    is_ocean = False

    @property
    def is_lake(self):
        return self.is_water and not self.is_ocean

    @property
    def is_coast(self):
        return any(vertex.is_ocean for vertex in self.vertices)

    def set_water_chance(self, noise_fn):
        water_chance = math.fabs(noise_fn(self.x * 3, self.y * 3))
        if self.distance_to_border() < 0.05:
            water_chance = max(water_chance - 0.5, 0)
        water_chance += (0.7 - math.sqrt(self.distance_to_map_centre())) * 0.5
        self.is_water = water_chance < 0.2

    def make_river(self, river_flow=1):
        self.river_flow += river_flow
        downstream_edge, downstream_vertex = self.get_downstream_edge()
        if not downstream_edge:
            return
        downstream_edge.river_flow += river_flow
        if not downstream_vertex.is_ocean:
            downstream_vertex.make_river(river_flow + 1)

    def get_downstream_edge(self):
        min_elevation = self.elevation
        min_edge = None
        min_vertex = None
        for edge in self.edges:
            other_vertex = edge.other_vertex(self)
            if other_vertex.elevation < min_elevation:
                min_edge = edge
                min_vertex = other_vertex
        if min_edge is None and not self.is_ocean:
            # We're ar at a local minima, which means a lake
            min_edge, min_vertex = self.find_downstream_lake_exit()

        return min_edge, min_vertex

    def find_downstream_lake_exit(self):
        open_set = set([vertex for vertex in self.vertices if vertex.is_water])
        lake_set = set()
        while open_set:
            vertex = open_set.pop()
            lake_set.add(vertex)
            open_set.update([
                _vertex for _vertex in vertex.vertices
                if _vertex.is_lake and _vertex not in lake_set
            ])

        edge_vertex_pairs = [
            (edge, edge.other_vertex(vertex))
            for vertex in lake_set
            for edge in vertex.edges
        ]

        min_elevation = self.elevation
        min_edge = None
        min_vertex = None
        for edge, vertex in edge_vertex_pairs:
            if vertex.elevation < min_elevation or vertex.is_ocean:
                min_edge, min_vertex = edge, vertex

        return min_edge, min_vertex


class Biome:
    BIOME_MAP = [
        ['desert', 'grassland', 'forest'],
        ['temperate_desert', 'grassland', 'deep_forest'],
        ['bare', 'tundra', 'snow']
    ]
    BIOME_COLOR_MAP = {
        'bare': colors.BARE_GREY,
        'deep_forest': colors.DEEP_FOREST_GREEN,
        'desert': colors.DESERT_BROWN,
        'forest': colors.FOREST_GREEN,
        'grassland': colors.GRASS_GREEN,
        'snow': colors.SNOW_WHITE,
        'temperate_desert': colors.TEMPERATE_DESERT_GREEN,
        'tundra': colors.TUNDRA_BEIGE,
        'beach': colors.SAND,
        'lake': colors.RIVER_BLUE
    }

    @classmethod
    def get_biome(cls, elevation, moisture):
        elevation_idx = min(int(elevation * 3), 2)
        moisture_idx = min(int(moisture * 3), 2)
        return cls.BIOME_MAP[elevation_idx][moisture_idx]

    def __init__(self, face):
        if face.is_coast:
            self.biome_type = 'beach'
        elif face.is_lake:
            self.biome_type = 'lake'
        else:
            self.biome_type = self.get_biome(face.elevation, face.moisture)

    @property
    def color(self):
        return self.BIOME_COLOR_MAP[self.biome_type]


PRIMITIVES = {
    'Face': MapFace,
    'Edge': MapEdge,
    'Vertex': MapVertex
}
