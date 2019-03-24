import pygame
import os
from modules.displayManager import displayManager
from objects.map import Map
from settings import settings
#from modules.mapManager import mapManager
#from modules.guiManager import guiManager
from objects.case import Case


class GameManager:

    def __init__(self):
        pass

    def init(self):
        displayManager.init()
        #mapManager.init()
        #guiManager.init()
        map = Map()
        map.generate_map((settings.TILE_HEIGHT, settings.TILE_WIDTH))
        self._cases = map.getMap()


    def start(self):
        clock = pygame.time.Clock()
        loop = True

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

            # Update
            # guiManager.updateGui()

            # Display
            displayManager.display(self._cases)
            # guiManager.displayGui()
            pygame.display.flip()

            clock.tick(20)


gameManager = GameManager()
