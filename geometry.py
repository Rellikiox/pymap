
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def scaled(self, scale):
        return Point(self.x * scale, self.y * scale)

    def int(self):
        return Point(int(self.x), int(self.y))

    def tuple(self):
        return (self.x, self.y)

    def to_pygame(self, scale):
        return self.scaled(scale).int().tuple()

    def dot_product(self, other_point):
        return self.x * other_point.x + self.y * other_point.y

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def slope(self, other_point):
        return (other_point.y - self.y) / (other_point.x - self.x)

    def out_of_bounds(self):
        return self.x < 0 or self.x > 1 or self.y < 0 or self.y > 1

    def distance_to_map_centre_normalized(self):
        vector_to_centre = Point(0.5, 0.5) - self
        return vector_to_centre.magnitude() / 0.708

    def __add__(self, other_point):
        return Point(self.x + other_point.x, self.y + other_point.y)

    def __sub__(self, other_point):
        return Point(self.x - other_point.x, self.y - other_point.y)

    def __truediv__(self, value):
        return Point(self.x / value, self.y / value)

    def __mul__(self, value):
        return Point(self.x * value, self.y * value)

    def __get__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError()

    def __repr__(self):
        return '<{},{}>'.format(self.x, self.y)

    def __str__(self):
        return '<{},{}>'.format(self.x, self.y)


class Triangle:

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.ab = None
        self.bc = None
        self.ca = None

    def centre(self):
        return (self.a + self.b + self.c) / 3

    def incentre(self):
        ab = (self.a - self.b).magnitude()
        bc = (self.b - self.c).magnitude()
        ca = (self.c - self.a).magnitude()
        return (self.a * bc + self.b * ca + self.c * ab) / (ab + bc + ca)

    def vertices(self):
        return [self.a, self.b, self.c]

    def set_neighbours(self, ab, bc, ca):
        if ab:
            self.ab = ab
        if bc:
            self.bc = bc
        if ca:
            self.ca = ca

    def neighbours(self):
        return [neighbour for neighbour in [self.ab, self.bc, self.ca] if neighbour is not None]

    def contains(self, point):
        """from http://blackpawn.com/texts/pointinpoly/"""
        # Compute vectors
        v0 = self.c - self.a
        v1 = self.b - self.a
        v2 = point - self.a

        # Compute dot products
        dot00 = v0.dot_product(v0)
        dot01 = v0.dot_product(v1)
        dot02 = v0.dot_product(v2)
        dot11 = v1.dot_product(v1)
        dot12 = v1.dot_product(v2)

        # Compute barycentric coordinates
        inverse_denominator = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inverse_denominator
        v = (dot00 * dot12 - dot01 * dot02) * inverse_denominator

        # Check if point is in triangle
        return (u >= 0) and (v >= 0) and (u + v < 1)

    def __str__(self):
        return '#{},{},{}#'.format(self.a, self.b, self.c)

    def __repr__(self):
        return '#{},{},{}#'.format(self.a, self.b, self.c)


class Region:
    def __init__(self, points):
        self.points = points

    def centre(self):
        centre = Point(0, 0)
        for point in self.points:
            centre += point
        return centre / len(self.points)
