from objects.enums.statsEnum import StatsEnum
from objects.enums.equipmentSlotsEnum import EquipmentSlotsEnum
import copy


class Entity(object):
    def __init__(self, name, equipments=None, gold=0, soul=0, level=0, experience=0,
                 baseStats=None, case=None, isPlayer=False, inventory=[], effects=[]):
        self._isPlayer = isPlayer
        self._case = case

        self._experience = experience
        self._nextLevelExperience = 100
        self._level = level
        self._name = name
        self._soul = soul
        self._gold = gold

        self._baseStats = {}
        for stat in StatsEnum:
            self._baseStats[stat] = baseStats[stat] if baseStats is not None and stat in baseStats else 0

        self._totalStats = copy.deepcopy(self._baseStats)
        self._equipments = {}
        for slot in EquipmentSlotsEnum:
            if equipments is not None and slot in equipments:
                self._equipments = equipments[slot]
                for stat in StatsEnum:
                    self._totalStats[stat] += equipments[slot].getBaseStats()[stat]
                # Subtract shield defense value ?
            else:
                self._equipments[slot] = None

        self._currentState = copy.deepcopy(self._totalStats)

        self._inventory = inventory
        self._effects = effects

    def getBaseStats(self):
        return self._baseStats

    def getCurrentState(self):
        return self._currentState

    def getCurrentHealth(self):
        return self._currentState[StatsEnum.HP]

    def getMaxHealth(self):
        return self._baseStats[StatsEnum.HP]

    def getCurrentMana(self):
        return self._currentState[StatsEnum.MANA]

    def getMaxMana(self):
        return self._baseStats[StatsEnum.MANA]

    def getCurrentXp(self):
        return self._experience

    def getNextLevelXp(self):
        return self._nextLevelExperience

    def equip(self):
        # Compute total stat
        pass

    def unequip(self):
        # Compute total stat
        pass