from objects.enums.statsEnum import StatsEnum
from objects.enums.effectTypesEnum import EffectTypesEnum

ALL_EFFECTS = [
  {
    'id': 'effect-1',
    'name': 'Heal over time',
    'duration': 3,
    'type': EffectTypesEnum.STATS_MODIFIER,
    'ratioPerStat': {
      StatsEnum.HP: 5
    }
  },
  {
    'id': 'effect-2',
    'name': 'Bleeding',
    'duration': 3,
    'type': EffectTypesEnum.STATS_MODIFIER,
    'ratioPerStat': {
      StatsEnum.HP: -5
    }
  },
  {
    'id': 'effect-3',
    'name': 'Atk Up',
    'duration': 5,
    'type': EffectTypesEnum.STATS_MODIFIER,
    'singleApplication': True,
    'ratioPerStat': {
      StatsEnum.ATK: 5
    }
  }
]