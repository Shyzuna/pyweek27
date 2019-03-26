from settings import settings
from settings.enums import Colors
from settings.enums import BiomesTypes

import modules.gameManager
import pygame
import os
import random

from objects.gui.basicButton import BasicButton
from objects.gui.basicBox import BasicBox
from objects.gui.basicLabel import BasicLabel
from objects.gui.textAlignEnum import HTextAlignEnum, VTextAlignEnum

class GuiManager(object):
    def __init__(self):
        self._fonts = {}
        self._lastMousePos = None
        self._onGuiElement = None

        self._testBtn = None
        self._box = None
        self._text = None

    def init(self):
        pygame.font.init()
        self._fonts['default'] = pygame.font.Font(os.path.join(settings.FONT_PATH, 'VCR_OSD.ttf'), 12)
        self._box = BasicBox(color=Colors.BLUE.value, position=(0.05, 0.05), size=(0.9, 0.9), windowBased=True)
        self._text = BasicLabel(font=self._fonts['default'], color=Colors.WHITE.value, text='Hello', parent=self._box,
                                position=(0.05, 0.05), size=(0.3, 0.3), vAlign=VTextAlignEnum.CENTER,
                                hAlign=HTextAlignEnum.CENTER)
        self._text.toggleDebug()
        self._testBtn = BasicButton(font=self._fonts['default'], baseColor=(128, 255, 0), hoveredColor=(128, 255, 128),
                                    selectedColor=(0, 255, 0), textColor=Colors.BLACK.value, text='Click to Hide',
                                    parent=self._box, position=(0.5, 0.8), size=(0.1, 0.1),
                                    clickHandler=self._box.toggleShow)
        self._testBtn.toggleDebug()

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

    def checkOnClick(self, value):
        if self._onGuiElement is not None:
            self._onGuiElement.onClick(value)

    def updateMousePos(self, mousePos):
        if self._lastMousePos != mousePos:
            self._lastMousePos = mousePos
            self._onGuiElement = self._box.checkInside(mousePos)

    def updateGui(self):
        self._box.update()

    def displayGui(self, screen):
        self._box.display(screen)


guiManager = GuiManager()
