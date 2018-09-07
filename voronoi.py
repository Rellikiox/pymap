
import grid
from geometry import Point
from scipy.spatial import Voronoi


DEFAULT_PRIMITIVES = {
    'Vertex': grid.Vertex,
    'Edge': grid.Edge,
    'Face': grid.Face
}


def get_voronoi(points, primitives=DEFAULT_PRIMITIVES):
    Face, Edge, Vertex = get_primitives(primitives)

    points.extend(get_bounding_box(points))
    voronoi = Voronoi([p.tuple() for p in points])

    vertices = [Vertex(*vertex) for vertex in voronoi.vertices]
    edges = [
        Edge([vertices[vertex_index] for vertex_index in ridge])
        for ridge in voronoi.ridge_vertices if -1 not in ridge
    ]
    faces = [
        Face([vertices[vertex_index] for vertex_index in region])
        for region in voronoi.regions if region and -1 not in region
    ]

    for edge in edges:
        edge.update_vertices_vertices()
        edge.update_faces_faces()

    for vertex in vertices:
        vertex.update_edges_edges()

    return faces, edges, vertices


def get_primitives(primitives):
    return [primitives.get(key) for key in ['Face', 'Edge', 'Vertex']]


def get_bounding_box(points):
    min_x = min(point.x for point in points)
    max_x = max(point.x for point in points)
    min_y = min(point.y for point in points)
    max_y = max(point.y for point in points)

    return [
        Point(min_x - 0.1, min_y - 0.1),
        Point(min_x - 0.1, max_y + 0.1),
        Point(max_x + 0.1, min_y - 0.1),
        Point(max_x + 0.1, max_y + 0.1)
    ]
