from objects.gui.guiElement import GuiElement
import pygame

class BasicBox(GuiElement):
    def __init__(self, color=None, *args, **kwargs):
        self._color = color
        self._surface = None
        super().__init__(*args, **kwargs)

    def redraw(self):
        super().redraw()
        self._surface = pygame.Surface(self._flatSize, flags=pygame.SRCALPHA)
        self._surface.fill(self._color)

    def ownDisplay(self, screen):
        screen.blit(self._surface, self._flatPosition)

    def setColor(self, color):
        self._color = color
        self._surface.fill(self._color)