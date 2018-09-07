
from grid import Face, Edge, Vertex
import colors


class MapFace(Face):
    is_ocean = False

    def color(self):
        if any(vertex.out_of_bounds() for vertex in self.vertices):
            return colors.OCEAN_BLUE

        return colors.color_in_range(
            colors.WHITE, colors.BLACK, self.centre.distance_to_map_centre_normalized()
        )

    @property
    def elevation_color(self):
        if self.is_ocean or any(vertex.water for vertex in self.vertices):
            return colors.OCEAN_BLUE
        return colors.MOUNTAIN_BROWN
        return colors.greyscale(self.elevation)

    @property
    def centre(self):
        return sum(self.vertices) / len(self.vertices)

    @property
    def elevation(self):
        return sum(vertex.elevation for vertex in self.vertices) / len(self.vertices)

    def is_on_border(self):
        return any(vertex.out_of_bounds() for vertex in self.vertices)


class MapEdge(Edge):
    pass


class MapVertex(Vertex):
    water = False

    def set_water(self, noise_fn):
        factor = (noise_fn(self.x, self.y) + 1) / 2

        # Make edges less likely
        distance_factor = max(self.distance_to_map_centre_normalized() - 0.5, 0)
        factor -= distance_factor
        self.water = factor < 0.45


PRIMITIVES = {
    'Face': MapFace,
    'Edge': MapEdge,
    'Vertex': MapVertex
}
