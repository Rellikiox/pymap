
import random
import math


def get_2d_points():

    open_points = set()
    points = list()
    min_radius = 0.05
    max_radius = 0.1

    open_points.add((random.random(), random.random()))

    while open_points:
        new_point_source = open_points.pop()
        points.append(new_point_source)

        for i in range(10):
            r = math.sqrt(random.random() * (max_radius**2 - min_radius**2) + min_radius**2)
            theta = random.uniform(0, 2 * math.pi)
            new_point = (
                new_point_source[0] + r * math.cos(theta),
                new_point_source[1] + r * math.sin(theta)
            )

            for point in points:
                if distance(point, new_point) < min_radius or out_of_bounds(new_point):
                    break
            else:
                open_points.add(new_point)

    return points


def distance(point_a, point_b):
    return math.hypot(point_a[0] - point_b[0], point_a[1] - point_b[1])


def out_of_bounds(point):
    return point[0] < 0 or point[1] < 0 or point[0] > 1 or point[1] > 1
