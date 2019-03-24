"""
Title: researchSettings File
Desc: All research settings
Creation Date: 26/10/17
LastMod Date: 26/10/17
TODO:
*
"""

from settings.enums import BiomesTypes


BIOMES_SETTINGS = {
    BiomesTypes.FOREST: {
        'repartition': 0.15,
        'repartition_delta': 0.05,
        'size_range': [2, 5]
    },
    BiomesTypes.DESERT: {
        'repartition': 0.25,
        'repartition_delta': 0.05,
        'size_range': [2, 5]
    },
    BiomesTypes.MOUNTAIN: {
        'repartition': 0.25,
        'repartition_delta': 0.05,
        'size_range': [2, 5]
    },
    BiomesTypes.PLAIN: {
        'repartition': 0.35,
        'repartition_delta': 0.05,
        'size_range': [2, 5]
    }
}