import pygame
import os
from settings import settings
from settings.enums import Colors


class DisplayManager:

    def __init__(self):
        pass

    def init(self):
        self.flags = pygame.DOUBLEBUF
        pygame.display.init()
        if settings.AUTO_SIZE:
            infoObject = pygame.display.Info()
            settings.SCREEN_WIDTH = infoObject.current_w - 200
            settings.SCREEN_HEIGHT = infoObject.current_h - 100
        settings.RECT_MAX_X = settings.MAP_WIDTH - settings.SCREEN_WIDTH
        settings.RECT_MAX_Y = settings.MAP_HEIGHT - settings.SCREEN_HEIGHT
        settings.SCROLL_MOUSE_MAX_X = settings.SCREEN_WIDTH - settings.SCROLL_MOUSE_MARGIN
        settings.SCROLL_MOUSE_MAX_Y = settings.SCREEN_HEIGHT - settings.SCROLL_MOUSE_MARGIN
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
                                              self.flags)
        pygame.display.set_caption("")

        self.createBaseMapSurface()
        self.loadImgs()

    def loadImgs(self):
        self.imgs = {}

        # Load hex images
        img = pygame.image.load(os.path.join(settings.HEX_PATH, "hexagon.png"))
        self.imgs["hex"] = pygame.transform.scale(img, (settings.TILE_WIDTH, settings.TILE_HEIGHT))

    def createBaseMapSurface(self):
        self.baseMapSurface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.baseMapSurface.fill(Colors.BLUE_OCEAN.value)

    def display(self, cases):
        self.screen.fill(Colors.WHITE.value)

        # Display background
        self.screen.blit(self.baseMapSurface, (0, 0))

        # Display cases
        for case in cases:
            self.screen.blit(self.imgs["hex"],
                             (case.getCenter(), case.getCenter()))


displayManager = DisplayManager()
