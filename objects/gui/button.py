import pygame
from settings.enums import Colors

class Button(object):
    def __init__(self, content='', img=None, color=None, hoverColor=None,
                 size=None, font=None, position=(0, 0), alpha=1):
        self._text = content
        self._textSurface = None
        self._textPos = None
        self._font = font
        self._position = position
        self._size = size if size is not None else img.get_size() if img is not None \
            else self._font.size(content) if content != '' else (0, 0)
        self._surface = None
        self._alpha = alpha * 255.0
        self._hoverColor = hoverColor
        self._color = color
        self._image = img

        self.render()

    def render(self):
        self._surface = pygame.Surface(self._size, flags=pygame.SRCALPHA)
        if self._color is not None:
            color = (self._color[0], self._color[1], self._color[2], self._alpha)
            self._surface.fill(color)
        if self._image is not None:
            self._surface.blit(self._image, (0, 0))

        if self._text != '':
            self._textSurface = self._font.render(self._text, True, Colors.BLACK.value)
            self._textPos = ((self._surface.get_width() - self._textSurface.get_width()) / 2,
                             (self._surface.get_height() - self._textSurface.get_height()) / 2)
            self._surface.blit(self._textSurface, self._textPos)

    def draw(self, screen):
        screen.blit(self._surface, self._position)