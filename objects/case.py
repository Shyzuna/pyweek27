from settings import settings
from settings import biomeSettings
from modules.utils import cubeRound
from modules.utils import cubeToOddQ
from objects.hex import Hex

import math


class Case(object):
    # Le repère de _position est axial (les deux axes sont q et r)
    # q est colinéaire à l'axe des abscisses
    # r est tourné de 60° dans le sens horaire
    def __init__(self, type, position=None, hex=None, selected=False):

        if position is not None:
            self._hex = Hex(position[0], position[1])
        elif hex is not None:
            self._hex = hex

        self._type = type
        self._selected = selected

    def getPosition(self):
        return self.getHex().getPosition()

    def getHex(self):
        return self._hex

    def getType(self):
        return self._type

    def setType(self, type):
        self._type = type

    def isWalkable(self):
        return biomeSettings.BIOMES_SETTINGS[self._type]['is_walkable']

    def draw(self, screen, img):
        # Offset entre le centre et le top left corner du sprite
        x = 1
        y = math.sqrt(3) / 2

        screen.blit(img,
                    ((settings.TILE_SIDE * (3 / 2 * self.getPosition()[0] - x)),
                     (settings.TILE_SIDE * (math.sqrt(3) * (self.getPosition()[1] + 0.5 * (self.getPosition()[0] & 1)) - y))))

    def draw2(self, screen, img, negativImg, baseH):
        # 3/4 of a case width
        xFactor = float(settings.TILE_WIDTH) * (3.0/4.0)
        # half of a case height + 10% of base height for overlapping
        yFactor = float(settings.TILE_WIDTH) / 2.0 - (baseH/10)
        # for image higher than default one
        yOffset = img.get_size()[1] - baseH

        screen.blit(img, (
            int(self.getPosition()[0] * xFactor),
            int(-yOffset + float(self.getPosition()[1]) * float(yFactor * 2)
                + (yFactor if self.getPosition()[0] % 2 == 1 else 0))
        ))
        if self._selected:
            screen.blit(negativImg, (
                int(self.getPosition()[0] * xFactor),
                int(-yOffset + float(self.getPosition()[1]) * float(yFactor * 2)
                    + (yFactor if self.getPosition()[0] % 2 == 1 else 0))
            ))

    def checkHover(self, pixel):
        return self.getHex().checkHover(pixel)

    def toggleSelected(self):
        self._selected = not self._selected