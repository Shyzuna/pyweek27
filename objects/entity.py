from objects.enums.statsEnum import StatsEnum
from objects.enums.equipmentSlotsEnum import EquipmentSlotsEnum
import copy


class Entity(object):
    def __init__(self, name, equipments=None, gold=0, soul=0, level=0, experience=0,
                 baseStats=None, case=None, isPlayer=False, inventory=[]):
        self._isPlayer = isPlayer
        self._case = case

        self._experience = experience
        self._level = level
        self._name = name
        self._soul = soul
        self._gold = gold

        self._baseStats = {}
        for stat in StatsEnum:
            self._equipments = baseStats[stat] if baseStats is not None and stat in baseStats else 0

        self._totalStats = copy.deepcopy(self._baseStats)
        self._equipments = {}
        for slot in EquipmentSlotsEnum:
            if equipments is not None and slot in equipments:
                self._equipments = equipments[slot]
                for stat in StatsEnum:
                    self._totalStats[stat] += equipments[slot].getBaseStats()[stat]
            else:
                self._equipments = equipments[slot] = None

        self._currentState = copy.deepcopy(self._totalStats)

        self._inventory = inventory
