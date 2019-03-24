from settings import settings
import math


class Case(object):
    def __init__(self, position, type):
        self._position = position
        self._type = type

    def getPosition(self):
        return self._position

    def getType(self):
        return self._type

    def draw(self, screen, img):
        screen.blit(img,
                    ((settings.TILE_SIDE * 3 / 2 * self.getPosition()[0]),
                     (settings.TILE_SIDE * math.sqrt(3) * (self.getPosition()[1] + 0.5 * (self.getPosition()[0] & 1)))))