# root elem should have a name
from objects.gui.basicBox import BasicBox
from objects.gui.guiElement import GuiElement
from objects.gui.basicButton import BasicButton
from objects.gui.basicLabel import BasicLabel
from objects.gui.linkedLabel import LinkedLabel
from objects.gui.progressBar import ProgressBar
from objects.entity import Entity
from objects.gui.textAlignEnum import HTextAlignEnum, VTextAlignEnum

import types

StatusPanelGUI = {
    0: [
        {
            'name': 'openButton',
            'elemType': BasicButton,
            'baseColor': (128, 255, 0, 200),
            'hoveredColor': (255, 255, 128, 100),
            'selectedColor': (0, 255, 0),
            'text': 'Open status',
            'position': (0.9, 0.1),
            'size': (0.1, 0.1),
            'windowBased': True
        },
        {
            'name': 'statusFrontElem',
            'elemType': GuiElement,
            'position': (0, 0.9),
            'size': (0.2, 0.1),
            'windowBased': True,
            'children': [
                {
                    'elemType': BasicBox,
                    'color': (100, 100, 100, 220),
                    'rounded': 0.2,
                    'position': (0.0, 0.0),
                    'size': (0.2, 0.33),
                    'children': [
                        {
                            'elemType': BasicLabel,
                            'text': 'HP',
                            'position': (0.0, 0.0),
                            'size': (1, 1),
                            'vAlign': VTextAlignEnum.CENTER,
                            'hAlign': HTextAlignEnum.CENTER
                        }
                    ]
                },
                {
                    'name': 'hpProgressBar',
                    'elemType': ProgressBar,
                    'currentRef': 'current',
                    'maxRef': 'max',
                    'position': (0.2, 0.0),
                    'size': (0.8, 0.33),
                    'refOptions': {
                        'max': {
                            'mandatory': True,
                            'type': types.MethodType
                        },
                        'current': {
                            'mandatory': True,
                            'type': types.MethodType
                        }
                    }
                },
                {
                    'elemType': BasicBox,
                    'color': (100, 100, 100, 220),
                    'rounded': 0.2,
                    'position': (0.0, 0.33),
                    'size': (0.2, 0.33),
                    'children': [
                        {
                            'elemType': BasicLabel,
                            'text': 'MANA',
                            'position': (0.0, 0.0),
                            'size': (1, 1),
                            'vAlign': VTextAlignEnum.CENTER,
                            'hAlign': HTextAlignEnum.CENTER
                        }
                    ]
                },
                {
                    'name': 'manaProgressBar',
                    'elemType': ProgressBar,
                    'currentRef': 'current',
                    'maxRef': 'max',
                    'position': (0.2, 0.33),
                    'size': (0.8, 0.33),
                    'barColor': (16, 171, 255),
                    'refOptions': {
                        'max': {
                            'mandatory': True,
                            'type': types.MethodType
                        },
                        'current': {
                            'mandatory': True,
                            'type': types.MethodType
                        }
                    }
                },
                {
                    'elemType': BasicBox,
                    'color': (100, 100, 100, 220),
                    'rounded': 0.2,
                    'position': (0.0, 0.66),
                    'size': (0.2, 0.33),
                    'children': [
                        {
                            'elemType': BasicLabel,
                            'text': 'XP',
                            'position': (0.0, 0.0),
                            'size': (1, 1),
                            'vAlign': VTextAlignEnum.CENTER,
                            'hAlign': HTextAlignEnum.CENTER
                        }
                    ]
                },
                {
                    'name': 'xpProgressBar',
                    'elemType': ProgressBar,
                    'currentRef': 'current',
                    'maxRef': 'max',
                    'position': (0.2, 0.66),
                    'size': (0.8, 0.33),
                    'barColor': (255, 237, 15),
                    'refOptions': {
                        'max': {
                            'mandatory': True,
                            'type': types.MethodType
                        },
                        'current': {
                            'mandatory': True,
                            'type': types.MethodType
                        }
                    }
                }
            ]
        }
    ],
    1: [
        {
            'name': 'statusPanel',
            'elemType': BasicBox,
            'color': (127, 127, 127, 220),
            'rounded': 0.1,
            'position': (0.15, 0.15),
            'size': (0.7, 0.7),
            'windowBased': True,
            'show': False,
            'children': [
                {
                    'name': 'closeButton',
                    'elemType': BasicButton,
                    'baseColor': (127, 0, 0, 200),
                    'hoveredColor': (180, 0, 0, 200),
                    'selectedColor': (0, 255, 0),
                    'text': 'X',
                    'position': (0.95, 0.02),
                    'size': (0.03, 0.05)
                },
                {
                    'name': 'charData',
                    'elemType': BasicBox,
                    'color': (100, 100, 100, 220),
                    'rounded': 0.1,
                    'position': (0.02, 0.05),
                    'size': (0.4, 0.3),
                    'children': [
                        {
                            'elemType': BasicLabel,
                            'text': 'Health Point',
                            'position': (0.05, 0.1),
                            'size': (0.9, 0.1)
                        },
                        {
                            'name': 'hpProgressBar',
                            'elemType': ProgressBar,
                            'currentRef': 'current',
                            'maxRef': 'max',
                            'position': (0.3, 0.1),
                            'size': (0.6, 0.1),
                            'refOptions': {
                                'max': {
                                    'mandatory': True,
                                    'type': types.MethodType
                                },
                                'current': {
                                    'mandatory': True,
                                    'type': types.MethodType
                                }
                            }
                        },
                        {
                            'elemType': BasicLabel,
                            'text': 'Mana Point',
                            'position': (0.05, 0.3),
                            'size': (0.9, 0.1)
                        },
                        {
                            'name': 'manaProgressBar',
                            'elemType': ProgressBar,
                            'currentRef': 'current',
                            'maxRef': 'max',
                            'position': (0.3, 0.3),
                            'size': (0.6, 0.1),
                            'barColor': (16, 171, 255),
                            'refOptions': {
                                'max': {
                                    'mandatory': True,
                                    'type': types.MethodType
                                },
                                'current': {
                                    'mandatory': True,
                                    'type': types.MethodType
                                }
                            }
                        },
                        {
                            'elemType': BasicLabel,
                            'text': 'Experience',
                            'position': (0.05, 0.5),
                            'size': (0.9, 0.1)
                        },
                        {
                            'name': 'xpProgressBar',
                            'elemType': ProgressBar,
                            'currentRef': 'current',
                            'maxRef': 'max',
                            'position': (0.3, 0.5),
                            'size': (0.6, 0.1),
                            'barColor': (255, 237, 15),
                            'refOptions': {
                                'max': {
                                    'mandatory': True,
                                    'type': types.MethodType
                                },
                                'current': {
                                    'mandatory': True,
                                    'type': types.MethodType
                                }
                            }
                        },
                        {
                            'name': 'linkedLevel',
                            'elemType': LinkedLabel,
                            'text': 'Level {player._level}',
                            'position': (0.05, 0.7),
                            'size': (0.9, 0.1),
                            'refOptions': {
                                'player': {
                                    'mandatory': True,
                                    'type': Entity
                                }
                            }
                        }
                    ]
                },
                {
                    'elemType': BasicBox,
                    'color': (100, 100, 100, 220),
                    'rounded': 0.1,
                    'position': (0.02, 0.4),
                    'size': (0.4, 0.55),
                    'children': [

                    ]
                },
                {
                    'elemType': BasicBox,
                    'color': (100, 100, 100, 220),
                    'rounded': 0.1,
                    'position': (0.46, 0.08),
                    'size': (0.52, 0.4),
                    'children': [

                    ]
                },
                {
                    'elemType': BasicBox,
                    'color': (100, 100, 100, 220),
                    'rounded': 0.1,
                    'position': (0.46, 0.53),
                    'size': (0.52, 0.42),
                    'children': [

                    ]
                }
            ]
        }
    ],
}