
from functools import partial

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEEP_BLUE = (9, 32, 84)
DARK_GREEN = (0, 64, 0)
DARKISH_GREEN = (0, 128, 0)
DARK_GREY = (128, 128, 128)
OCEAN_BLUE = (175, 214, 254)
MOUNTAIN_BROWN = (58, 48, 40)
SAND = (169, 159, 138)
RIVER_BLUE = (71, 139, 253)

BARE_GREY = (152, 152, 152)
DEEP_FOREST_GREEN = (87, 138, 112)
DESERT_BROWN = (208, 192, 155)
FOREST_GREEN = (110, 166, 100)
GRASS_GREEN = (149, 180, 113)
SNOW_WHITE = (248, 248, 248)
TEMPERATE_DESERT_GREEN = (151, 165, 138)
TUNDRA_BEIGE = (218, 221, 187)


def color_in_range(start_color, end_color, percentage):
    return tuple(
        [int(start + (end - start) * percentage) for start, end in zip(start_color, end_color)]
    )


greyscale = partial(color_in_range, BLACK, WHITE)
