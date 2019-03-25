from settings import settings
from settings.enums import Colors

import modules.gameManager
import pygame
import os

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

    def checkMousePosition(self, point):
        # Check cases
        case = modules.gameManager.gameManager.getCaseAt(point)

        if case is not None:
            print(case.getPosition())
        else:
            print("Le curseur n'est pas sur une case")

    def displayGui(self, screen):
        self._testBtn.draw(screen)


guiManager = GuiManager()
