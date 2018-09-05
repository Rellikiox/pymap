
import datetime
import os
import pygame.display
import pygame.draw
import pygame.transform
import sys

import grid
import delaunay
from geometry import Point


WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 128)
DARK_GREEN = (0, 64, 0)
DARKISH_GREEN = (0, 128, 0)
DARK_GREY = (128, 128, 128)
OCEAN_BLUE = (175, 214, 254)
GRASS_GREEN = (189, 237, 174)
MOUNTAIN_BROWN = (58, 48, 40)
MAP_SCALE = 900


def region_color(region):
	distance_to_centre = (Point(0.5, 0.5) - region.centre()).magnitude()
	color = tuple([int(start + (end - start) * distance_to_centre) for start, end in zip(GRASS_GREEN, MOUNTAIN_BROWN)])
	return color


def main():
	screen = setup_and_get_screen()
	screen = draw(screen)
	save_image(screen)


def draw(screen):
	points = grid.get_fuzzy_grid(60, 60)
	regions, ridges = delaunay.voronoi(points)
	for region in regions:
		pygame.draw.polygon(screen, region_color(region), [point.to_pygame(MAP_SCALE) for point in region.points])
	# for ridge in ridges:
	# 	pygame.draw.line(screen, DARK_GREY, ridge[0].to_pygame(MAP_SCALE), ridge[1].to_pygame(MAP_SCALE))

	return screen


def setup_and_get_screen():
	# set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
	os.environ["SDL_VIDEODRIVER"] = "dummy"
	pygame.display.init()
	screen = pygame.display.set_mode((MAP_SCALE,MAP_SCALE), 0, 32)
	screen.fill(OCEAN_BLUE)
	return screen


def save_image(screen):
	pygame.display.update()
	timestamp = datetime.datetime.now().strftime('%Y.%m.%dT%H.%M.%S')
	filename = 'screenshots/{}.png'.format(timestamp)
	pygame.image.save(screen, filename)

if __name__ == "__main__":
	main()