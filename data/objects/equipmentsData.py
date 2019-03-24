from objects.enums.statsEnum import StatsEnum
from objects.enums.effectTypesEnum import EffectTypesEnum
from objects.enums.equipmentTypesEnum import EquipmentTypesEnum
from objects.enums.equipmentSlotsEnum import EquipmentSlotsEnum

ALL_EQUIPMENTS = [
    {
        'id': 'weapon-1',
        'type': EquipmentTypesEnum.LWEAPON,
        'slotType': [EquipmentSlotsEnum.LEFT_HAND, EquipmentSlotsEnum.RIGHT_HAND],
        'stats': {
            StatsEnum.ATK: 10
        },
        'range': 1,
        'size': 1,
        'ratio': '[ATK]*1.2',
        'actionCost': 2,
        'effects': ['effect-3'],
        'value': 10,
        'lootable': True
    }
]