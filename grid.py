
from geometry import Point


class Face:
    # Faces it's connected to
    faces = None
    # Edges it's surrounded by
    edges = None
    # Points on its perimeter
    vertices = None

    def __init__(self, vertices):
        self.faces = []
        self.edges = []
        self.vertices = vertices

        self.update_edges()
        self.update_edges_faces()
        self.update_vertices_faces()

    def update_edges(self):
        all_edges = [edge for vertex in self.vertices for edge in vertex.edges]
        self.edges = [
            edge for edge in all_edges
            if all_edges.count(edge) == 2
        ]

    def update_edges_faces(self):
        for edge in self.edges:
            edge.faces.append(self)

    def update_vertices_faces(self):
        for vertex in self.vertices:
            vertex.faces.append(self)


class Edge:
    # The faces this edge is connected to
    faces = None
    # Edges that share a vertex
    edges = None
    # The two vertices of this edge
    vertices = None

    def __init__(self, vertices):
        self.faces = []
        self.edges = []
        self.vertices = vertices

        self.update_vertices_edges()

    def update_vertices_edges(self):
        for vertex in self.vertices:
            vertex.edges.append(self)

    def update_vertices_vertices(self):
        vertex_a, vertex_b = self.vertices
        vertex_a.vertices.append(vertex_b)
        vertex_b.vertices.append(vertex_a)

    def update_faces_faces(self):
        for face in self.faces:
            face.faces.extend([_face for _face in self.faces if _face != face])


class Vertex(Point):
    # The faces this vertex is part of
    faces = None
    # The edges this vertex is part of
    edges = None
    # The vertices that share an edge
    vertices = None

    def __init__(self, *args):
        super().__init__(*args)
        self.faces = []
        self.edges = []
        self.vertices = []

    def update_edges_edges(self):
        for edge in self.edges:
            edge.edges.extend([_edge for _edge in self.edges if _edge != edge])
