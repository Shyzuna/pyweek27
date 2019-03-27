from settings import settings
from settings.enums import Colors
from settings.enums import BiomesTypes

import modules.gameManager
import pygame
import os
import random

from objects.gui.guiElement import GuiElement
from objects.gui.basicButton import BasicButton
from objects.gui.basicBox import BasicBox
from objects.gui.basicLabel import BasicLabel
from objects.gui.textAlignEnum import HTextAlignEnum, VTextAlignEnum

# /!\ Element on same layer shouldn't intersect

class GuiManager(object):
    def __init__(self):
        self._fonts = {}
        self._lastMousePos = None
        self._onGuiElement = None

        self._guiElementId = 0

        # 5 layers by default
        self._maxLayer = 4
        self._layers = [{} for x in range(0, self._maxLayer + 1)]

    def init(self):
        pygame.font.init()
        self._fonts['default'] = pygame.font.Font(os.path.join(settings.FONT_PATH, 'VCR_OSD.ttf'), 12)

        box = BasicBox(color=(127, 127, 127, 220), rounded=0.1, position=(0.05, 0.05), size=(0.9, 0.9), windowBased=True, name='menu')
        text = BasicLabel(font=self._fonts['default'], color=Colors.WHITE.value, text='Hello', parent=box,
                                position=(0.05, 0.05), size=(0.3, 0.3), vAlign=VTextAlignEnum.CENTER,
                                hAlign=HTextAlignEnum.CENTER)
        box.toggleDebug()
        box.toggleShow()
        text.toggleDebug()
        testBtn = BasicButton(font=self._fonts['default'], baseColor=(128, 255, 0), hoveredColor=(128, 0, 0),
                                    selectedColor=(0, 255, 0), textColor=Colors.BLACK.value, text='Click to Hide',
                                    parent=box, position=(0.5, 0.8), size=(0.1, 0.1), name='closeMenu')
        testBtn.toggleDebug()
        self.addToLayer(box, 1)
        dicti = {
            0: [
                {
                    'name': 'button',
                    'elemType': BasicButton,
                    'font': self._fonts['default'],
                    'baseColor': (128, 255, 0, 200),
                    'hoveredColor': (255, 255, 128, 100),
                    'selectedColor': (0, 255, 0),
                    'textColor': Colors.BLACK.value,
                    'text': 'Hello',
                    'position': (0.9, 0.1),
                    'size': (0.1, 0.1),
                    'windowBased': True
                }
            ]
        }
        self.guiLoader(dicti)
        self._layers[0]['button'].addEventHandler('click', box.toggleShow, 'displayBox')
        self._layers[1]['menu'].getChildNamedInHierarchy('closeMenu').addEventHandler('click', box.toggleShow, 'hideBox')

    def getElementGuiId(self):
        self._guiElementId += 1
        return self._guiElementId

    def addToLayer(self, guiElem, layer):
        if layer > self._maxLayer:
            return
        self._layers[layer][guiElem.getName()] = guiElem

    def checkMousePosition(self, pixel):
        # Check cases
        map = modules.gameManager.gameManager.getMap()
        case = map.getCaseAtPixel(pixel)

        if case is None:
            print("Le curseur n'est pas sur une case")
            return None

        # Test getNeighbours
        #neighbours = map.getCaseNeighbours(case)
        # Test getSpiralRing
        #ring = map.getCaseSpiralRing(case, 2)
        # Test getShortestPath
        # path = map.getShortestPath(case.getPosition(), map.getCaseAtPos((2, 2)).getPosition())
        # Test getVisibleCases
        visible_cases = map.getVisibleCases(case, 3)

        # Change neighbours type
        # if a path has been found
        if visible_cases is not None:
            type = random.choice([BiomesTypes.PLAIN, BiomesTypes.FOREST, BiomesTypes.DESERT])
            for _case in visible_cases:
               _case._type = type

    def checkOnClick(self, value):
        if self._onGuiElement is not None:
            self._onGuiElement.onClick(value)

    def updateMousePos(self, mousePos):
        # small bug here showing new element without moving (Maybe force when new display)
        if self._lastMousePos != mousePos:
            self._lastMousePos = mousePos
            self._onGuiElement = None

            for l in range(self._maxLayer, -1, -1):
                for guiElem in self._layers[l].values():
                    self._onGuiElement = guiElem.checkInside(mousePos)
                    if self._onGuiElement is not None:
                        return

    def updateGui(self):
        for l in range(0, self._maxLayer + 1):
            for guiElem in self._layers[l].values():
                guiElem.update()

    def displayGui(self, screen):
        for l in range(0, self._maxLayer + 1):
            for guiElem in self._layers[l].values():
                guiElem.display(screen)

    def guiLoader(self, dictio):
        for layer, elements in dictio.items():
            print(layer)
            print(elements)
            currentLayer = int(layer)
            if layer > self._maxLayer or layer < 0:
                raise ValueError('Invalid layer value')
            for elem in elements:
                guiElem = self.guiNodeCreator(elem)
                self.addToLayer(guiElem, currentLayer)

    def guiNodeCreator(self, node, parent=None):
        if 'elemType' not in node.keys():
            raise KeyError('No key named "elemType"')
        elemType = node['elemType']  # Add white list for elem type ?
        del node['elemType']
        if not issubclass(elemType, GuiElement):
            raise TypeError('Invalid element type')

        children = None
        if 'children' in node.keys():
            children = node['children']
            del node['children']

        guiElem = elemType(parent=parent, **node)
        if children is not None:
            for child in children:
                self.guiNodeCreator(child, parent=guiElem)
        return guiElem


guiManager = GuiManager()
