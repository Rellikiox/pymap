
from operator import attrgetter
from grid import Point
from scipy.spatial import Delaunay
from geometry import Triangle, Point


def triangulate(points):
	delaunay = Delaunay([p.tuple() for p in points])

	triangles = [
		Triangle(points[idx_a], points[idx_b], points[idx_c])
		for idx_a, idx_b, idx_c in delaunay.simplices
	]
	for triangle, neighbours in zip(triangles, delaunay.neighbors):
		triangle_neighbours = [triangles[index] if index != -1 else None for index in neighbours]
		triangle.set_neighbours(*triangle_neighbours)

	return triangles


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
