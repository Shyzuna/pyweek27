from settings import settings
from settings.enums import Colors
from settings.enums import BiomesTypes

import modules.gameManager
import pygame
import os
import random

from objects.gui.button import Button

class GuiManager(object):
    def __init__(self):
        self._fonts = {}
        self._testBtn = None

    def init(self):
        pygame.font.init()
        self._fonts['default'] = pygame.font.Font(os.path.join(settings.FONT_PATH, 'VCR_OSD.ttf'), 12)
        self._testBtn = Button(content='Bonjour', color=Colors.LIGHT_GREY.value,
                               font=self._fonts['default'], size=(100, 50), alpha=0.8)

    def checkMousePosition(self, pixel):
        # Check cases
        case = modules.gameManager.gameManager.getCaseAtPixel(pixel)

        if case is None:
            print("Le curseur n'est pas sur une case")
            return None

        # Test getNeighbours
        neighbours = modules.gameManager.gameManager.getCaseNeighbours(case)
        # Test getSpiralRing
        ring = modules.gameManager.gameManager.getCaseSpiralRing(case, 2)

        # Change neighbours type
        type = random.choice(list(BiomesTypes))
        for _case in ring:
            _case._type = type



    def displayGui(self, screen):
        self._testBtn.draw(screen)


guiManager = GuiManager()
