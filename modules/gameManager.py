import pygame
import os
from modules.displayManager import displayManager
from objects.map import Map
from settings import settings
#from modules.mapManager import mapManager
from modules.guiManager import guiManager
from objects.case import Case
from objects.hex import Hex
from modules import utils

oddq_directions = [
    # Pour les colonnes paires
    [Hex(0, -1), Hex(+1, -1), Hex(+1, 0),
     Hex(0, +1), Hex(-1, 0), Hex(-1, -1)],
    # Pour les colonnes impaires
    [Hex(0, -1), Hex(+1, 0), Hex(+1, +1),
     Hex(-1, +1), Hex(0, +1), Hex(-1, 0)]
]

class GameManager:

    def __init__(self):
        pass

    def init(self):
        displayManager.init()
        #mapManager.init()
        guiManager.init()
        map = Map((settings.TILES_NUM_HEIGHT, settings.TILES_NUM_WIDTH))
        map.generate()
        print(map.findAPath((1,1), (6,6)))
        self._cases = map.getMap()


    def start(self):
        clock = pygame.time.Clock()
        loop = True

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    guiManager.checkMousePosition(pygame.mouse.get_pos())

            # Update
            # guiManager.updateGui()

            # Display
            displayManager.display(self._cases)
            guiManager.displayGui(displayManager.screen)
            pygame.display.flip()

            clock.tick(settings.FPS)

    def getCases(self):
        return self._cases

    def getCaseAtPos(self, pos):
        for case in self.getCases():
            if case.getPosition() == pos:
                return case
        # Not found
        return None

    def getCaseAtPixel(self, point):
        for case in self.getCases():
            if case.checkHover(point):
                return case
        # Not found
        return None

    def getCaseNeighbours(self, case):
        neighbours = []
        # On choisit les bonnes directions en fonction de la parité sur la colonne
        directions = oddq_directions[case.getHex().getQ() & 1]

        for direction in directions:
            for _case in self.getCases():
                if (case.getHex() + direction).getPosition() == _case.getPosition():
                    neighbours.append(_case)

        return neighbours

    def getCaseRing(self, case, radius):
        x, y, z = utils.oddQToCube(case.getHex().getQ(), case.getHex().getR())
        cubeResults = utils.cubeRing(x, y, z, radius)
        results = []
        for cubeResult in cubeResults:
            x, y, z = cubeResult
            for case in self.getCases():
                if utils.cubeToOddQ(x, y, z) == case.getPosition():
                    results.append(case)

        return results

    def getCaseSpiralRing(self, case, radius):
        x, y, z = utils.oddQToCube(case.getHex().getQ(), case.getHex().getR())
        cubeResults = utils.cubeSpiral(x, y, z, radius)
        results = []

        for cubeResult in cubeResults:
            x, y, z = cubeResult
            for case in self.getCases():
                if utils.cubeToOddQ(x, y, z) == case.getPosition():
                    results.append(case)

        return results


gameManager = GameManager()
