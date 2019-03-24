from objects.enums.statsEnum import StatsEnum


class Equipment(object):
    def __init__(self, name, elemType, ratio=0, slotType=[], baseStats=None, range=0, size=0, lootable=False, value=0):
        self._name = name
        self._elemType = elemType
        self._slotType = slotType

        self._baseStats = {}
        for stat in StatsEnum:
            self._equipments = baseStats[stat] if baseStats is not None and stat in baseStats else 0

        self._range = range
        self._size = size
        self._ratio = ratio

        self._lootable = lootable
        self._value = value

    def getBaseStats(self):
        return self._baseStats