import pygame

# Put hover state here !
# try to do some handler biding

class GuiElement(object):
    def __init__(self, position=(0, 0), size=(0, 0), parent=None,
                 flatPos=False, flatSize=False, windowBased=False, debug=False):
        self._show = True
        self._position = position
        self._flatPosition = None
        self._size = size
        self._flatSize = None
        self._flatRect = None
        self._parent = parent
        self._debug = False
        self._debugSurface = None
        self._debugOptions = {
            'color': (255, 0, 255),
            'width': 2
        }
        if self._parent is not None:
            self._parent.addChild(self)
        self._children = []
        self._options = {
            'flatPos': flatPos,
            'flatSize': flatSize,
            'windowBased': windowBased
        }
        self._insideElement = False
        self._clickIn = False
        self.resize()

    def toggleShow(self):
        self._show = not self._show

    def getSize(self):
        return self._size

    def getPosition(self):
        return self._position

    def getFlatSize(self):
        return self._flatSize

    def getFlatPosition(self):
        return self._flatPosition

    def toggleDebug(self):
        self._debug = not self._debug

    def resize(self):
        screen_size = pygame.display.get_surface().get_size()
        parent_size = self._parent.getFlatSize() if self._parent is not None else \
            screen_size if self._options['windowBased'] else (0, 0)
        if not self._options['flatSize']:
            self._flatSize = (self._size[0] * parent_size[0], self._size[1] * parent_size[1])
        else:
            self._flatSize = self._size

        parent_pos = self._parent.getFlatPosition() if self._parent is not None else (0, 0)
        if not self._options['flatPos']:
            self._flatPosition = (self._position[0] * parent_size[0] + parent_pos[0],
                                  self._position[1] * parent_size[1] + parent_pos[1])
        else:
            self._flatPosition = (self._position[0] + parent_pos[0], self._position[1] + parent_pos[1])
        self._flatRect = pygame.Rect(self._flatPosition[0], self._flatPosition[1], self._flatSize[0], self._flatSize[1])
        self.redraw()

    def redraw(self):
        self.redrawDebug()

    def redrawDebug(self):
        self._debugSurface = pygame.Surface((self._flatSize[0] + self._debugOptions['width'] * 2,
                                             self._flatSize[1] + self._debugOptions['width'] * 2),
                                            flags=pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, self._flatSize[0] + self._debugOptions['width'],
                           self._flatSize[1] + self._debugOptions['width'])
        pygame.draw.rect(self._debugSurface, self._debugOptions['color'], rect, 2)

    def display(self, screen):
        if not self._show:
            return
        self.ownDisplay(screen)
        if self._debug:
            self.debugDisplay(screen)
        self.displayChildren(screen)

    def debugDisplay(self, screen):
        screen.blit(self._debugSurface, (self._flatPosition[0] - self._debugOptions['width'],
                                         self._flatPosition[1] - self._debugOptions['width']))

    def ownDisplay(self, screen):
        pass

    def displayChildren(self, screen):
        for child in self._children:
            child.display(screen)

    def addChild(self, child):
        self._children.append(child)

    def checkInside(self, mousePos):
        wasInside = self._insideElement
        self._insideElement = False
        currentElem = None
        if self._show and self._flatRect.collidepoint(mousePos):
            currentElem = self
            for child in self._children:
                result = child.checkInside(mousePos)
                currentElem = result if result is not None else currentElem
            if currentElem == self:
                self._insideElement = True
        if wasInside and wasInside != self._insideElement:
            # Layer system will make this buggy when dragging moose from top layer to down layer
            self._clickIn = False
        return currentElem

    def update(self):
        if not self._show:
            return
        self.ownUpdate()
        self.childrenUpdate()

    def ownUpdate(self):
        pass

    def childrenUpdate(self):
        for child in self._children:
            child.update()

    def onClick(self, value):
        if value:
            self._clickIn = True
        else:
            if self._clickIn:
                self._clickIn = False
                self.onClickHandler()

    def onClickHandler(self):
        pass