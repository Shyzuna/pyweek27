from objects.gui.guiElement import GuiElement
from objects.gui.textAlignEnum import HTextAlignEnum, VTextAlignEnum

class BasicLabel(GuiElement):
    def __init__(self, color=(0, 0, 0), text='', font='default', hAlign=HTextAlignEnum.LEFT,
                 vAlign=VTextAlignEnum.TOP, *args, **kwargs):
        self._text = text
        self._color = color
        self._font = font
        self._textSurface = None
        self._vAlign = vAlign
        self._hAlign = hAlign
        print(font)
        super().__init__(*args, **kwargs)

    def redraw(self):
        super().redraw()
        self._textSurface = self._fonts[self._font].render(self._text, True, self._color)

    def ownDisplay(self, screen):
        textSize = self._textSurface.get_size()
        position = (
            (0 if self._hAlign == HTextAlignEnum.LEFT else (self._flatSize[0] - textSize[0])
            if self._hAlign == HTextAlignEnum.RIGHT else (self._flatSize[0] - textSize[0]) / 2) + self._flatPosition[0],
            (0 if self._vAlign == VTextAlignEnum.TOP else (self._flatSize[1] - textSize[1])
            if self._vAlign == VTextAlignEnum.BOTTOM else (self._flatSize[1] - textSize[1]) / 2) + self._flatPosition[1]
        )
        screen.blit(self._textSurface, position)

    def setText(self, text):
        self._text = text
        self.redraw()