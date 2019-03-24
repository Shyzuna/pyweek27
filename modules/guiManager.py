from settings import settings

import modules.gameManager
import pygame


class GuiManager(object):
    def __init__(self):
        pass

    def init(self):
        pass

    def checkMousePosition(self, point):
        # Check cases
        case = modules.gameManager.gameManager.getCaseAt(point)

        if case is not None:
            print(case.getPosition())
        else:
            print("Le curseur n'est pas sur une case")


guiManager = GuiManager()
