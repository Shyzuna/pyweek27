import pygame
import os
from settings import settings
from settings.enums import Colors, BiomesTypes
import math


class DisplayManager:

    def __init__(self):
        self.screen = None
        self._negativImgs = {}
        self._imgs = {}

        self._baseH = 0

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
        pygame.display.set_caption("666")

        self.createBaseMapSurface()
        self.loadImgs()

    def loadImgs(self):
        # Load hex images
        for biome in BiomesTypes:
            try:
                img = pygame.image.load(os.path.join(settings.HEX_PATH, str(biome.value) + ".png"))
                #self.imgs[biome.value] = pygame.transform.scale(img, (settings.TILE_WIDTH, settings.TILE_HEIGHT))
                #self.imgs[biome.value] = pygame.transform.scale(img, (img.get_size()[0]*3, img.get_size()[1]*3))
                factor = float(settings.TILE_WIDTH)/float(img.get_size()[0])
                self._imgs[biome.value] = pygame.transform.scale(img, (settings.TILE_WIDTH, int(img.get_size()[1] * factor)))

                # create
                self._negativImgs[biome.value] = self._imgs[biome.value].copy()
                self._negativImgs[biome.value].fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_MAX)
                self._negativImgs[biome.value].fill((255, 255, 255, 120), special_flags=pygame.BLEND_RGBA_MIN)
            except Exception as e:
                print(e)
                #pass
        self._baseH = self._imgs[0].get_size()[1]

    def getImages(self):
        return self._imgs

    def getBaseH(self):
        return self._baseH

    def getNegativImages(self):
        return self._negativImgs

    def createBaseMapSurface(self):
        self.baseMapSurface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.baseMapSurface.fill(Colors.BLUE_OCEAN.value)

    def display(self, map):
        self.screen.fill(Colors.WHITE.value)

        # Display background
        self.screen.blit(self.baseMapSurface, (0, 0))

        # Display cases
        # i = 0
        # for case in map.getCases():
        #     case.draw(self.screen, self.imgs[case.getType().value])
        #     i += 1
        #     if i == 15:
        #         return
        map.displayMap(self.screen, self._baseH)



displayManager = DisplayManager()
