
import datetime
import os
import pygame.display
import pygame.draw
import pygame.transform
import sys

import poisson_disc


WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 128)


def main():
	screen = setup_and_get_screen()
	screen = draw(screen)
	save_image(screen)


def draw(screen):
	points = poisson_disc.get_2d_points()
	for point in points:
		screen.set_at((int(point[0] * 512), int(point[1] * 512)), DARK_BLUE)

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
	filename = '{}.jpg'.format(timestamp)
	pygame.image.save(screen, filename)

if __name__ == "__main__":
	main()