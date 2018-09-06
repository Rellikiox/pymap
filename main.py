
import datetime
import os

from map import Map
import pygame.display
import pygame.draw
import pygame.transform


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 128)
DARK_GREEN = (0, 64, 0)
DARKISH_GREEN = (0, 128, 0)
DARK_GREY = (128, 128, 128)
OCEAN_BLUE = (175, 214, 254)
GRASS_GREEN = (189, 237, 174)
MOUNTAIN_BROWN = (58, 48, 40)
MAP_SCALE = 900


def main():
    screen = setup_and_get_screen()
    Map().draw(screen)
    save_image(screen)


def setup_and_get_screen():
    # set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.display.init()
    screen = pygame.display.set_mode((MAP_SCALE, MAP_SCALE), 0, 32)
    screen.fill(OCEAN_BLUE)
    return screen


def save_image(screen):
    pygame.display.update()
    timestamp = datetime.datetime.now().strftime('%Y.%m.%dT%H.%M.%S')
    filename = 'screenshots/{}.png'.format(timestamp)
    pygame.image.save(screen, filename)


def color_in_range(start_color, end_color, percentage):
    return tuple(
        [int(start + (end - start) * percentage) for start, end in zip(start_color, end_color)]
    )


if __name__ == "__main__":
    main()


class Cell:
    def __init__(self, region):
        self.region = region
        self.centre = region.centre()

    def color(self):
        if any(point.out_of_bounds() for point in self.region.points):
            return OCEAN_BLUE

        color = color_in_range(WHITE, BLACK, self.centre.distance_to_map_centre_normalized())
        return color
