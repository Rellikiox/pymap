
import random
from geometry import Point


def get_grid(width, height):
    return [
        Point(i / (width - 1), j / (height - 1))
        for j in range(height)
        for i in range(width)
    ]


def get_fuzzy_grid(width, height):
    max_random_offset = 0.6
    max_x_random_offset = max_random_offset / (width - 1)
    max_y_random_offset = max_random_offset / (height - 1)

    grid = [
        Point(i / (width - 1), j / (height - 1))
        for j in range(height)
        for i in range(width)
    ]
    for point in grid:
        if point_on_edge(point):
            continue
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


def point_on_edge(point):
    return point.x == 0 or point.x == 1 or point.y == 0 or point.y == 1
