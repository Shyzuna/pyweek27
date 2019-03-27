import pygame
from objects.gui.guiElement import GuiElement
from objects.gui.basicLabel import BasicLabel
from objects.gui.basicBox import BasicBox
from objects.gui.textAlignEnum import HTextAlignEnum, VTextAlignEnum

class BasicButton(GuiElement):
    def __init__(self, font, baseColor, hoveredColor, selectedColor,
                 textColor, text='', *args, **kwargs):
        self._baseColor = baseColor
        self._hoveredColor = hoveredColor
        self._selectedColor = selectedColor
        self._label = BasicLabel(font, textColor, text, hAlign=HTextAlignEnum.CENTER,
                                 vAlign=VTextAlignEnum.CENTER, *args, **kwargs)
        self._box = BasicBox(baseColor, rounded=0.2, *args, **kwargs)
        self._hovered = False
        super().__init__(*args, **kwargs)

    def ownUpdate(self):
        if self._insideElement != self._hovered:
            self._hovered = self._insideElement
            self._box.setColor(self._hoveredColor if self._hovered else self._baseColor)

    def redraw(self):
        # can be optimized
        super().redraw()
        self._label.redraw()
        self._box.redraw()

    def ownDisplay(self, screen):
        self._box.display(screen)
        self._label.display(screen)

    #  May move this in parent class
    def onClickHandler(self):
        if 'click' in self._eventsHandlers.keys():
            for handler in self._eventsHandlers['click'].values():
                handler()
