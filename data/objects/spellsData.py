from objects.enums.spellTypesEnum import SpellTypesEnum

ALL_SPELLS = [
  {
    'id': 'spell-1',
    'name': 'Boule de feu',
    'type': SpellTypesEnum.ATK,
    'ratio': '10',
    'range': 2,
    'size': 1,
    'actionCost': 2,
    'value': 10,
    'lootable': True
  },
  {
    'id': 'spell-2',
    'name': 'Healu',
    'type': SpellTypesEnum.HEAL,
    'ratio': '10',
    'actionCost': 2,
    'value': 10,
    'lootable': True,
    'effects': ['effect-1']
  }
]