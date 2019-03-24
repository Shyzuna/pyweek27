
class Spell(object):
    def __init__(self, name, spellType, ratio=0, manaCost=0,
                 actionCost=0, range=0, size=0, lootable=False, value=0, linkedEffects=[]):
        self._name = name
        self._spellType = spellType

        self._ratio = ratio
        self._manaCost = manaCost
        self._actionCost = actionCost

        self._range = range
        self._size = size

        self._lootable = lootable
        self._value = value

        self._linkedEffects = linkedEffects
