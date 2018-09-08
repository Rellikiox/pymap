
from functools import partial

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEEP_BLUE = (9, 32, 84)
DARK_GREEN = (0, 64, 0)
DARKISH_GREEN = (0, 128, 0)
DARK_GREY = (128, 128, 128)
OCEAN_BLUE = (175, 214, 254)
GRASS_GREEN = (222, 244, 215)
FOREST_GREEN = (4, 153, 19)
MOUNTAIN_BROWN = (58, 48, 40)
SAND = (223, 187, 138)
RIVER_BLUE = (71, 139, 253)


def color_in_range(start_color, end_color, percentage):
    return tuple(
        [int(start + (end - start) * percentage) for start, end in zip(start_color, end_color)]
    )


greyscale = partial(color_in_range, BLACK, WHITE)
