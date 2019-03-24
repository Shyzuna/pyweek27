from enum import Enum


class Colors(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREY = (125, 125, 125)
    LIGHT_GREY = (200, 200, 200)
    LIGHT_CYAN = (14, 174, 204)
    GREEN = (0, 255, 0)
    BLUE_OCEAN = (9, 127, 217)

class BiomesTypes(Enum):
    FOREST = 0
    DESERT = 1
    MOUNTAIN = 2
    PLAIN = 3

