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
        self._map = map


    def start(self):
        clock = pygame.time.Clock()
        loop = True

        while loop:

            guiManager.updateMousePos(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    guiManager.checkMousePosition(pygame.mouse.get_pos())
                    guiManager.checkOnClick(True)
                elif event.type == pygame.MOUSEBUTTONUP:
                    guiManager.checkOnClick(False)

            # Update
            guiManager.updateGui()

            # Display
            displayManager.display(self.getMap())
            guiManager.displayGui(displayManager.screen)
            pygame.display.flip()

            clock.tick(settings.FPS)

    def getMap(self):
        return self._map


gameManager = GameManager()
