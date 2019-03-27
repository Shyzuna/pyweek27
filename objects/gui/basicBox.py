from objects.gui.guiElement import GuiElement
import pygame

class BasicBox(GuiElement):
    def __init__(self, color=None, rounded=0, *args, **kwargs):
        self._color = color
        self._surface = None
        self._savedSurface = None
        self._rounded = rounded
        super().__init__(*args, **kwargs)

    def redraw(self):
        super().redraw()
        self._surface = pygame.Surface(self._flatSize, flags=pygame.SRCALPHA)
        if self._rounded > 0:
            myRect = self._surface.get_rect()
            circle = pygame.Surface([min(self._flatSize)*3]*2, pygame.SRCALPHA)
            pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
            circle = pygame.transform.smoothscale(circle, [int(min(self._flatSize) * self._rounded)] * 2)
            rect = self._surface.blit(circle, (0, 0))
            rect.bottomright = myRect.bottomright
            self._surface.blit(circle, rect)
            rect.topright = myRect.topright
            self._surface.blit(circle, rect)
            rect.bottomleft = myRect.bottomleft
            self._surface.blit(circle, rect)
            self._surface.fill((0, 0, 0), myRect.inflate(-rect.w, 0))
            self._surface.fill((0, 0, 0), myRect.inflate(0, -rect.h))
            self._savedSurface = self._surface.copy()
            subColor = pygame.Color(*self._color)
            alpha = subColor.a
            subColor.a = 0
            self._surface.fill(subColor, special_flags=pygame.BLEND_RGBA_MAX)
            self._surface.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)
        else:
            self._surface.fill(self._color)

    def ownDisplay(self, screen):
        screen.blit(self._surface, self._flatPosition)

    def setColor(self, color):
        self._color = color
        if self._rounded > 0:
            self._surface = self._savedSurface.copy()
            subColor = pygame.Color(*self._color)
            alpha = subColor.a
            subColor.a = 0
            self._surface.fill(subColor, special_flags=pygame.BLEND_RGBA_MAX)
            self._surface.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)
        else:
            self._surface.fill(self._color)
