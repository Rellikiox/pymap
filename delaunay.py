
from operator import attrgetter
from grid import Point
from scipy.spatial import Delaunay, Voronoi
from geometry import Triangle, Point, Region


def voronoi(points):
	voronoi = Voronoi([p.tuple() for p in points])

	regions =  [
		Region([Point(*voronoi.vertices[index]) for index in region])
		for region in voronoi.regions if len(region) >= 1 and -1 not in region
	]
	ridges = [
		(Point(*voronoi.vertices[ridge[0]]), Point(*voronoi.vertices[ridge[1]]))
		for ridge in voronoi.ridge_vertices if -1 not in ridge
	]
	return regions, ridges


def delaunay(points):
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
