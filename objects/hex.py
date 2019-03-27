from settings import settings
from modules.utils import cubeRound
from modules.utils import cubeToOddQ

import math


class Hex(object):
    # Le repère de _position est axial (les deux axes sont q et r)
    # q est colinéaire à l'axe des abscisses
    # r est tourné de 30° dans le sens horaire
    def __init__(self, q, r):
        self._q = q
        self._r = r

    def getQ(self):
        return self._q

    def getR(self):
        return self._r

    def getPosition(self):
        return self._q, self._r

    def checkHover(self, point):
        q = ( 2/3 * point[0]) / settings.TILE_SIDE
        r = (-1/3 * point[0] + math.sqrt(3)/3 * point[1]) / settings.TILE_SIDE

        x, y, z = cubeRound(q, -q-r, r)
        col, row = cubeToOddQ(x, y, z)
        #print("Coordonnees trouvees: ({},{}) pour le clic a ({},{})".format(col, row, point[0], point[1]))

        return (col, row) == (self.getQ(), self.getR())

    # Surcharges d'opérateurs
    # Additionne les deux vecteurs de positions
    def __add__(self, hex):
        return Hex(self.getQ() + hex.getQ(), self.getR() + hex.getR())

    # Soustrait le vecteur de position du paramètre hex à cette hex
    def __sub__(self, hex):
        return Hex(self.getQ() - hex.getQ(), self.getR() - hex.getR())

