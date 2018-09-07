
import datetime
import os
import sys

from map import Map
import pygame.display
import pygame.draw
import pygame.transform
import random

MAP_SCALE = 900


def main(seed):
    screen = setup_and_get_screen()
    Map(seed).draw(screen, MAP_SCALE)
    save_image(screen)


def setup_and_get_screen():
    # set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.display.init()
    screen = pygame.display.set_mode((MAP_SCALE, MAP_SCALE), 0, 32)

    return screen


def save_image(screen):
    pygame.display.update()
    timestamp = datetime.datetime.now().strftime('%Y.%m.%dT%H.%M.%S')
    filename = 'screenshots/{}.png'.format(timestamp)
    pygame.image.save(screen, filename)


if __name__ == "__main__":
    seed = sys.argv[1] if len(sys.argv) > 1 else random.randint(0, sys.maxsize)
    main(seed)
