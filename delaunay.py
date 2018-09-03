
from operator import attrgetter
from grid import Point

class Triangle:
	@staticmethod
	def bilateral_connect(triangle_a, triangle_b):
		triangle_a.connect(triangle_b)
		triangle_b.connect(triangle_a)

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

	def circumcircle(self):
		# Radius
		ab = (self.a - self.b).magnitude()
		bc = (self.b - self.c).magnitude()
		ca = (self.c - self.a).magnitude()
		radius = ab * bc * ca / math.sqrt(
			(ab + bc + ca) * (bc + ca - ab) * (ca + ab - bc) * (ab + bc - ca)
		)
		# Centre
		mid_ab = (self.a + self.b) / 2
		mid_bc = (self.b + self.c) / 2
		ab_slope = (self.a.y - self.b.y) / (self.a.x - self.b.x)
		bc_slope = (self.b.y - self.c.y) / (self.b.x - self.c.x)


	def vertices(self):
		return [self.a, self.b, self.c]

	def neighbours(self):
		return [neighbour for neighbour in [self.ab, self.bc, self.ca] if neighbour is not None]

	def connect(self, other_triangle):
		vertices = other_triangle.vertices()
		a_shared = self.a in vertices
		b_shared = self.b in vertices
		c_shared = self.c in vertices
		if a_shared and b_shared:
			self.ab = other_triangle
		elif b_shared and c_shared:
			self.bc = other_triangle
		elif c_shared and a_shared:
			self.ca = other_triangle

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

	def explode(self, point):
		abp = Triangle(self.a, self.b, point)
		bcp = Triangle(self.b, self.c, point)
		cap = Triangle(self.c, self.a, point)

		# if self.ab:
		# 	if Point.in_circumdisk(self.a, self.b, point):


		Triangle.bilateral_connect(abp, bcp)
		Triangle.bilateral_connect(bcp, cap)
		Triangle.bilateral_connect(cap, abp)

		if self.ab:
			Triangle.bilateral_connect(abp, self.ab)
		if self.bc:
			Triangle.bilateral_connect(bcp, self.bc)
		if self.ca:
			Triangle.bilateral_connect(cap, self.ca)



		return [abp, bcp, cap]

	def other_point(self, point_a, point_b):
		if self.a in [point_a, point_b] and self.b in [point_a, point_b]:
			return self.c
		if self.b in [point_a, point_b] and self.c in [point_a, point_b]:
			return self.a
		if self.c in [point_a, point_b] and self.a in [point_a, point_b]:
			return self.b

	def __str__(self):
		return '#{},{},{}#'.format(self.a, self.b, self.c)

	def __repr__(self):
		return '#{},{},{}#'.format(self.a, self.b, self.c)


def triangulate(points):
	# bb_points = get_bounding_box(points)
	bb_points = [Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)]
	triangulation = [
		Triangle(bb_points[0], bb_points[1], bb_points[2]),
		Triangle(bb_points[1], bb_points[2], bb_points[3])
	]
	Triangle.bilateral_connect(triangulation[0], triangulation[1])
	# points = [Point(0.25, 0.25), Point(0.75, 0.75)]
	# for point in points:
	# 	# Find triangle that contains point
	# 	triangle = next(triangle for triangle in triangulation if triangle.contains(point))
	# 	new_triangles = triangle.explode(point)
	# 	triangulation.remove(triangle)
	# 	triangulation.extend(new_triangles)


	return triangulation


def get_bounding_box(points):
	min_x = min(point.x for point in points)
	max_x = max(point.x for point in points)
	width = max_x - min_x
	min_y = min(point.y for point in points)
	max_y = max(point.y for point in points)
	height = max_y - min_y

	return [
		Point(min_x - 0.1, min_y - 0.1),
		Point(min_x - 0.1, max_y + 0.1),
		Point(max_x + 0.1, min_y - 0.1),
		Point(max_x + 0.1, max_y + 0.1)
	]
