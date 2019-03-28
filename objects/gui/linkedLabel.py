import pygame
from objects.gui.guiElement import GuiElement
from objects.gui.basicLabel import BasicLabel
from objects.gui.textAlignEnum import HTextAlignEnum, VTextAlignEnum

class LinkedLabel(GuiElement):
    def __init__(self, textColor=(0, 0, 0), font='default', text='',
                 hAlign=HTextAlignEnum.LEFT, vAlign=VTextAlignEnum.TOP, *args, **kwargs):
        self._baseText = text
        self._label = BasicLabel(font=font, color=textColor, text=text, hAlign=hAlign, vAlign=vAlign, *args, **kwargs)
        super().__init__(*args, **kwargs)
        self._formattedText = ''
        self.formatText()
        self.addEventHandler('newRef', self.formatText, 'textFormat')

    def redraw(self):
        # can be optimize
        super().redraw()
        self.formatText()

    def ownDisplay(self, screen):
        self._label.display(screen)

    def formatText(self):
        # something better ?
        formatRef = self.getFormattedReferences()
        if formatRef is not None:
            self._formattedText = self._baseText.format(**formatRef)
        else:
            self._formattedText = self._baseText
        self._label.setText(self._formattedText)
