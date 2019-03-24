import pygame
import os
from modules.displayManager import displayManager
from settings import settings
#from modules.mapManager import mapManager
from modules.guiManager import guiManager
from objects.case import Case


class GameManager:

    def __init__(self):
        pass

    def init(self):
        displayManager.init()
        #mapManager.init()
        guiManager.init()
        self._cases = []
        self._cases.append(Case((0, 0)))
        self._cases.append(Case((0, 1)))
        self._cases.append(Case((0, 2)))
        self._cases.append(Case((0, 3)))
        self._cases.append(Case((1, 0)))
        self._cases.append(Case((2, 0)))
        self._cases.append(Case((3, 0)))
        self._cases.append(Case((4, 0)))

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
            # guiManager.displayGui()
            pygame.display.flip()

            clock.tick(settings.FPS)

    def getCases(self):
        return self._cases

    def getCaseAt(self, point):
        for case in self.getCases():
            if case.checkHover(point):
                return case
        # Not found
        return None


gameManager = GameManager()
