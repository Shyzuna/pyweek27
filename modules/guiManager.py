from settings import settings
from settings.enums import Colors
from settings.enums import BiomesTypes

import modules.gameManager
import pygame
import os
import random

from data.gui.statusPanelGui import StatusPanelGUI

from objects.gui.guiElement import GuiElement
from objects.gui.basicButton import BasicButton
from objects.gui.basicBox import BasicBox
from objects.gui.basicLabel import BasicLabel
from objects.gui.textAlignEnum import HTextAlignEnum, VTextAlignEnum

# /!\ Element on same layer shouldn't intersect
# Loader for references and events handlers

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
        self._fonts['default'] = pygame.font.Font(os.path.join(settings.FONT_PATH, 'VCR_OSD.ttf'), 15)

        self.guiLoader(StatusPanelGUI)

        self._layers[0]['openButton'].addEventHandler('click', self._layers[1]['statusPanel'].toggleShow, 'displayBox')
        statusPanel = self._layers[1]['statusPanel']
        statusPanel.getChildNamedInHierarchy('closeButton').addEventHandler('click', statusPanel.toggleShow, 'close')

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

        # Change neighbours type
        #type = random.choice(list(BiomesTypes))
        #for _case in ring:
        #    _case._type = type

        path = map.getShortestPath(case.getPosition(), map.getCaseAtPos((2, 2)).getPosition())
        # Change neighbours type
        type = random.choice(list(BiomesTypes))
        for _case in path:
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
            currentLayer = int(layer)
            if layer > self._maxLayer or layer < 0:
                raise ValueError('Invalid layer value')
            for elem in elements:
                guiElem = self.guiNodeCreator(elem)
                self.addToLayer(guiElem, currentLayer)

    def guiNodeCreator(self, node, parent=None):
        print(node)
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

        guiElem = elemType(parent=parent, fonts=self._fonts, **node)
        if children is not None:
            for child in children:
                self.guiNodeCreator(child, parent=guiElem)
        return guiElem


guiManager = GuiManager()
