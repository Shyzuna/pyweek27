from objects.entity import Entity
from objects.equipment import Equipment
from objects.enums.equipmentSlotsEnum import EquipmentSlotsEnum
from objects.enums.statsEnum import StatsEnum
from objects.enums.equipmentTypesEnum import EquipmentTypesEnum

if __name__ == '__main__':
    sword = Equipment('Sword', EquipmentTypesEnum.LWEAPON, ratio='ATK*1.2',
                      slotType=[EquipmentSlotsEnum.RIGHT_HAND, EquipmentSlotsEnum.LEFT_HAND],
                      range=1, size=1, actionCost=1)

    player = Entity('Player', equipments={EquipmentSlotsEnum.RIGHT_HAND: sword}, isPlayer=True,
                    baseStats={StatsEnum.HP: 10, StatsEnum.DEF: 5, StatsEnum.MANA: 5, StatsEnum.ACTION: 4})