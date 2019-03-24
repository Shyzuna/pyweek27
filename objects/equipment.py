from objects.enums.statsEnum import StatsEnum


class Equipment(object):
    def __init__(self, name, elemType, ratio=0, slotType=[], baseStats=None,
                 range=0, size=0, lootable=False, value=0, actionCost = 0, linkedEffects=[]):

        # Add linked ability ?
        # Add linked buffs/debuffs ?

        self._name = name
        self._elemType = elemType
        self._slotType = slotType

        self._baseStats = {}
        for stat in StatsEnum:
            self._baseStats[stat] = baseStats[stat] if baseStats is not None and stat in baseStats else 0

        self._range = range
        self._size = size
        self._ratio = ratio

        self._lootable = lootable
        self._value = value
        self._actionCost = actionCost

        self._linkedEffects = linkedEffects
        self._affectedBy = []

    def getBaseStats(self):
        return self._baseStats