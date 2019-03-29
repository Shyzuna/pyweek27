import pygame
import types
# Put hover state here !
# Do smth better for event handler
# improve references

class GuiElement(object):

    uniqueId = 0

    def __init__(self, position=(0, 0), size=(0, 0), parent=None, show=True, fonts=None, refOptions={},
                 flatPos=False, flatSize=False, windowBased=False, debug=False, name=None):
        self._show = show
        self._position = position
        self._flatPosition = None
        self._size = size
        self._flatSize = None
        self._flatRect = None
        self._parent = parent
        self._debug = debug
        self._debugSurface = None
        self._fonts = fonts
        self._debugOptions = {
            'color': (255, 0, 255),
            'width': 2
        }
        if name is None:
            GuiElement.uniqueId += 1
            self._name = name if name is not None else '{}-{}'.format(str(type(self)), str(GuiElement.uniqueId))
        else:  # doesn't check for same name in hierarchy
            self._name = name
        if self._parent is not None:
            self._parent.addChild(self)
        self._children = {}
        self._options = {
            'flatPos': flatPos,
            'flatSize': flatSize,
            'windowBased': windowBased
        }
        self._watchedValues = {}
        self._watchers = {}
        self._insideElement = False
        self._clickIn = False

        self._eventsHandlers = {}
        self._references = {}
        self._refOptions = refOptions

        self.addEventHandler('redraw', self.redraw, 'redraw')

        self.resize()

    def toggleShow(self):
        self._show = not self._show
        self.callEvent('show' if self._show else 'hide')

    def getSize(self):
        return self._size

    def setSize(self, size):
        self._size = size

    def getPosition(self):
        return self._position

    def getFlatSize(self):
        return self._flatSize

    def getFlatPosition(self):
        return self._flatPosition

    def getName(self):
        return self._name

    def getChildren(self):
        return self._children

    def getChildNamed(self, name):
        if name in self._children.keys():
            return self._children[name]
        return None

    def getChildNamedInHierarchy(self, name, level=None):
        level = level if level is not None else self
        children = level.getChildren()
        if name in children.keys():
            return children[name]
        for child in children.values():
            res = self.getChildNamedInHierarchy(name, child)
            if res is not None:
                return res
        return None

    #  Maybe not removable ...
    def addWatcher(self, func, name, event='redraw'):
        print(func)
        self._watchers[name] = event
        return watcherDecorator(func, name, self.myWatcher)

    def myWatcher(self, name, value):
        if not name in self._watchedValues.keys() or self._watchedValues[name] != value:
            self._watchedValues[name] = value
            self.callEvent(self._watchers[name])

    #  Add remove if needed
    def addReference(self, name, ref):
        self._references[name] = ref
        self.callEvent('newRef')

    def addReferences(self, refs):
        for name, ref in refs.items():
            self._references[name] = ref
        self.callEvent('newRef')

    #  Add remove if needed
    def addEventHandler(self, event, handler, name):
        if event not in self._eventsHandlers.keys():
            self._eventsHandlers[event] = {}
        self._eventsHandlers[event][name] = handler

    def getFormattedReferences(self):
        # check ref options
        formatRef = {}
        for key, value in self._refOptions.items():
            if key not in self._references.keys():
                if 'mandatory' in value.keys():
                    print("Missing mandatory reference {} for gui element.".format(key))
                    return None
            else:
                if 'type' not in value.keys() or not isinstance(self._references[key], value['type']):
                    print("Invalid type of reference {} for gui element.".format(key))
                    return None
                formatRef[key] = self._references[key]() if isinstance(self._references[key], types.FunctionType) or\
                                                            isinstance(self._references[key], types.MethodType) else self._references[key]
        return formatRef

    def callEvent(self, event):
        if event in self._eventsHandlers.keys():
            for handler in self._eventsHandlers[event].values():
                handler()

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

    def redrawChildren(self):
        for child in self._children.values():
            child.redraw()

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
        for child in self._children.values():
            child.display(screen)

    def addChild(self, child):
        self._children[child.getName()] = child

    def checkInside(self, mousePos):
        wasInside = self._insideElement
        self._insideElement = False
        currentElem = None
        if self._show and self._flatRect.collidepoint(mousePos):
            currentElem = self
            for child in self._children.values():
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
        for child in self._children.values():
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

# used to decorate on the fly for watcher
def watcherDecorator(func, name, watcher):
    def wrapper(value):
        func(value)
        watcher(name, value)
    return wrapper
