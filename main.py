
import datetime
import os
import sys

from map import Map
import pygame.display
import pygame.font
import pygame.draw
import pygame.transform
import random

MAP_SCALE = 900


def create_map(seed=None, draw_mode='map'):
    seed = seed if seed is not None else str(random.randint(0, sys.maxsize))
    screen = setup_and_get_screen()
    map = Map(MAP_SCALE, seed)
    map.create()
    font = pygame.font.SysFont('Comic Sans MS', 12)
    map.draw(screen, MAP_SCALE, font, draw_mode)
    save_image(screen)


def setup_and_get_screen():
    # set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.font.init()
    pygame.display.init()
    screen = pygame.display.set_mode((MAP_SCALE, MAP_SCALE), 0, 32)

    return screen


def save_image(screen):
    pygame.display.update()
    timestamp = datetime.datetime.now().strftime('%Y.%m.%dT%H.%M.%S')
    filename = 'screenshots/{}.png'.format(timestamp)
    pygame.image.save(screen, filename)
    filename = 'static/latest_screenshot.png'
    pygame.image.save(screen, filename)


if __name__ == "__main__":
    seed = sys.argv[1] if len(sys.argv) > 1 else None
    create_map(seed)
