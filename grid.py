
import random
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
		return self.scaled(512).int().tuple()
		
	def dot_product(self, other_point):
		return self.x * other_point.x + self.y * other_point.y
		
	def magnitude(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)

	@staticmethod
	def in_circumdisk(point_a, point_b, other_point):
		circumdisk_centre = (point_b + point_a) / 2 
		circumdisk_radius = (circumdisk_centre - point_a).magnitude()
		return (other_point - circumdisk_centre).magnitude() < circumdisk_radius

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


def get_grid(width, height):
	return [
		Point(i / (width - 1), j / (height - 1)) 
		for j in range(height)
		for i in range(width)
	]



def get_fuzzy_grid(width, height):
	max_random_offset = 0.4
	max_x_random_offset = max_random_offset / (width - 1)
	max_y_random_offset = max_random_offset / (height - 1)

	grid = [
		Point(i / (width - 1), j / (height - 1)) 
		for j in range(height)
		for i in range(width)
	]
	for point in grid:
		point.x += (random.random() * 2 - 1) * max_x_random_offset
		point.y += (random.random() * 2 - 1) * max_y_random_offset

	min_x = min(point.x for point in grid)
	max_x = max(point.x for point in grid)
	x_scale = max_x - min_x
	min_y = min(point.y for point in grid)
	max_y = max(point.y for point in grid)
	y_scale = max_y - min_y

	for point in grid:
		point.x = (point.x - min_x) / x_scale
		point.y = (point.y - min_y) / y_scale

	return grid
