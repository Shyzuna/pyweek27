from settings import settings
from modules.utils import cubeRound
from modules.utils import cubeToOddQ


import math


class Case(object):

    def __init__(self, position, type):
        self._position = position
        self._type = type

    def getPosition(self):
        return self._position

    def getType(self):
        return self._type

    def setType(self, type):
        self._type = type

    def draw(self, screen, img):
        # Offset entre le centre et le top left corner du sprite
        x = 1
        y = math.sqrt(3) / 2

        screen.blit(img,
                    ((settings.TILE_SIDE * (3 / 2 * self.getPosition()[0] - x)),
                     (settings.TILE_SIDE * (math.sqrt(3) * (self.getPosition()[1] + 0.5 * (self.getPosition()[0] & 1)) - y))))

    def checkHover(self, point):
        q = ( 2/3 * point[0]) / settings.TILE_SIDE
        r = (-1/3 * point[0] + math.sqrt(3)/3 * point[1]) / settings.TILE_SIDE

        x, y, z = cubeRound(q, -q-r, r)
        col, row = cubeToOddQ(x, y, z)
        print("Coordonnees trouvees: ({},{}) pour le clic a ({},{})".format(col, row, point[0], point[1]))

        return (col, row) == self.getPosition()





