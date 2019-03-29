import pygame
from objects.gui.guiElement import GuiElement
from objects.gui.linkedLabel import LinkedLabel
from objects.gui.basicBox import BasicBox
from objects.gui.textAlignEnum import HTextAlignEnum, VTextAlignEnum

class ProgressBar(GuiElement):
    def __init__(self, currentRef, maxRef, barColor=(255, 0, 0), bgColor=(255, 255, 255), textColor=(0, 0, 0),
                 font='default', *args, **kwargs):
        # Ref option should match currentRef & maxRef
        self._bgBox = BasicBox(color=bgColor, rounded=0.4, *args, **kwargs)
        self._frontBox = BasicBox(color=barColor, rounded=0.4,  parent=self._bgBox)
        self._label = LinkedLabel(textColor=textColor, font=font, text='{' + currentRef + '}/{' + maxRef + '}',
                                  vAlign=VTextAlignEnum.CENTER, hAlign=HTextAlignEnum.CENTER, *args, **kwargs)
        super().__init__(*args, **kwargs)
        self._currentRef = currentRef
        self._maxRef = maxRef
        self._percent = None
        self.addEventHandler('newRef', self.computePercent, 'computePercent')

    def redraw(self):
        # can be optimize
        super().redraw()
        self._bgBox.redraw()
        self.computePercent()

    def ownDisplay(self, screen):
        self._bgBox.display(screen)
        self._label.display(screen)

    def computePercent(self):
        formatRef = self.getFormattedReferences()
        if formatRef is not None:
            # Ref option should match currentRef & maxRef
            current = int(formatRef[self._currentRef])
            max = int(formatRef[self._maxRef])
            if max > 0:
                self._percent = float(current)/float(max)
                self._frontBox.setSize((self._percent, 1))
                self._frontBox.resize()
                self._label.addReferences(self._references)
