
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
        return colors.OCEAN_BLUE if self.water else colors.MOUNTAIN_BROWN

    @property
    def centre(self):
        return sum(self.vertices) / len(self.vertices)

    @property
    def water(self):
        return len([vertex for vertex in self.vertices if not vertex.water]) <= 1

    @property
    def factor(self):
        return sum(vertex.factor for vertex in self.vertices) / len(self.vertices)

    @property
    def elevation(self):
        return sum(vertex.elevation for vertex in self.vertices) / len(self.vertices)

    def is_on_border(self):
        return any(vertex.out_of_bounds() for vertex in self.vertices)


class MapEdge(Edge):
    pass

import noise, math

class MapVertex(Vertex):
    elevation = None

    def set_water(self, noise_fn):
        if self.distance_to_border() < 0.1:
            self.factor = 0
        else:
            self.factor = (noise_fn(self.x, self.y) + 1) / 2
            # Make edges less likely
            distance = self.distance_to_map_centre()
            if distance > 0.65:
                self.factor = self.factor - 0.5
            else:
                self.factor = self.factor - math.sqrt(distance) * 0.3

    @property
    def water(self):
        return self.new_factor < 0.2

    def set_new_factor(self, base):
        self.new_factor = math.fabs(noise.pnoise2(self.x * 3, self.y * 3, octaves=4, base=base))
        if self.distance_to_border() < 0.05:
            self.new_factor = max(self.new_factor - 0.5, 0)
        self.new_factor = self.new_factor + (0.7 - math.sqrt(self.distance_to_map_centre()))
        # self.new_factor = max(min(self.new_factor * (2 - distance_to_map_centre_factor), 1), 0)


PRIMITIVES = {
    'Face': MapFace,
    'Edge': MapEdge,
    'Vertex': MapVertex
}
