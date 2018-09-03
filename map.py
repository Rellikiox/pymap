
import datetime
import os
import pygame.display
import pygame.draw
import pygame.transform
import sys

import grid
import delaunay


WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 128)
DARK_GREEN = (0, 64, 0)
DARKISH_GREEN = (0, 128, 0)
DARK_RED = (128, 0, 0)


def main():
	screen = setup_and_get_screen()
	screen = draw(screen)
	save_image(screen)


def draw(screen):
	points = grid.get_fuzzy_grid(3, 3)
	triangulation = delaunay.triangulate(points)
	for triangle in triangulation:
		pygame.draw.circle(screen, DARK_GREEN, triangle.centre().to_pygame(512), int((triangle.centre() - triangle.a).scaled(512).magnitude()), 1)
		pygame.draw.circle(screen, DARK_GREEN, triangle.centre().to_pygame(512), 2)
		for neighbour in triangle.neighbours():
			pygame.draw.line(screen, DARKISH_GREEN, triangle.incentre().to_pygame(512), neighbour.incentre().to_pygame(512), 1)

		# pygame.draw.polygon(screen, DARK_BLUE, [point.to_pygame(512) for point in triangle.vertices()], 2)
	# for point in points:
	# 	pygame.draw.circle(screen, DARK_BLUE, point.to_pygame(512), 2)

	return screen


def setup_and_get_screen():
	# set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
	os.environ["SDL_VIDEODRIVER"] = "dummy"
	pygame.display.init()
	screen = pygame.display.set_mode((512,512))
	screen.fill(WHITE)
	return screen


def save_image(screen):
	pygame.display.update()
	timestamp = datetime.datetime.now().strftime('%Y.%m.%dT%H.%M.%S')
	filename = '{}.png'.format(timestamp)
	pygame.image.save(screen, filename)

if __name__ == "__main__":
	main()