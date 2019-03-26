
import numpy

from settings.enums import BiomesTypes
from settings import biomeSettings
from objects.case import Case

class Map:
    TILES_DIRECTION = [
        [[+1, 0], [+1, -1], [0, -1],
         [-1, -1], [-1, 0], [0, +1]],
        [[+1, +1], [+1, 0], [0, -1],
         [-1, 0], [-1, +1], [0, +1]],
    ]

    def __init__(self):
        self._map = []

    def generate_map(self, mapSize):
        totalTiles = mapSize[0] * mapSize[1]
        tilesRepartition = {}
        tempMap = {}
        tilesLeft = []

        # Init map
        print("Taille totale %s" % totalTiles)
        for i in range(1, mapSize[0] + 1):
            tempMap.update({i: {}})
            for j in range(1, mapSize[1] + 1):
                tempMap[i].update({j: -1})
                tilesLeft.append((i, j))

        # Compute tiles repartition
        randomTotalTiles = 0
        for biome in BiomesTypes:
            delta = numpy.random.uniform(-biomeSettings.BIOMES_SETTINGS[biome]['repartition_delta'],
                                         biomeSettings.BIOMES_SETTINGS[biome]['repartition_delta'])
            tilesNum = int(totalTiles * (biomeSettings.BIOMES_SETTINGS[biome]['repartition'] - delta))
            tilesRepartition.update({biome: tilesNum})
            randomTotalTiles += tilesNum

        if randomTotalTiles < totalTiles:
            randLastTye = numpy.random.randint(0, len(BiomesTypes))
            tilesRepartition[BiomesTypes(randLastTye)] += totalTiles - randomTotalTiles

        print(tilesRepartition)

        # Fill map
        while len(tilesLeft) > 0:
            for tile in tilesLeft:
                row_index = tile[0]
                col_index = tile[1]
                if tempMap[row_index][col_index] == -1:
                    print("Case %s %s non traitée" % (row_index, col_index))
                    biome = BiomesTypes(numpy.random.randint(0, len(BiomesTypes)))
                    batchSize = numpy.random.randint(biomeSettings.BIOMES_SETTINGS[biome]['size_range'][0],
                                                     biomeSettings.BIOMES_SETTINGS[biome]['size_range'][1] + 1)

                    while tilesRepartition[biome] == 0:
                        biome = BiomesTypes(numpy.random.randint(0, len(BiomesTypes)))
                        batchSize = numpy.random.randint(biomeSettings.BIOMES_SETTINGS[biome]['size_range'][0],
                                                         biomeSettings.BIOMES_SETTINGS[biome]['size_range'][1] + 1)

                    if batchSize > tilesRepartition[biome]:
                        batchSize = tilesRepartition[biome]

                    print("Taille du batch %s de type %s" % (batchSize, biome))

                    tempMap[row_index][col_index] = biome
                    batchElements = [(row_index, col_index)]
                    batchSize -= 1
                    tilesRepartition[biome] -= 1
                    tilesLeft.remove((row_index, col_index))

                    # Chose neighbor
                    numRetries = 40
                    while batchSize > 0 and numRetries >= 0:
                        neighbor = numpy.random.randint(0, len(batchElements))

                        while True:
                            if (batchElements[neighbor][0] % 2) > 0:
                                next_pos = Map.TILES_DIRECTION[1][numpy.random.randint(0, 6)]
                            else:
                                next_pos = Map.TILES_DIRECTION[0][numpy.random.randint(0, 6)]

                            next_tile_row = batchElements[neighbor][0] + next_pos[0]
                            next_tile_col = batchElements[neighbor][1] + next_pos[1]

                            if next_tile_row >= 1 and next_tile_row <= mapSize[0] \
                                and next_tile_col >= 1 and next_tile_col <= mapSize[1]:
                                break

                        if tempMap[next_tile_row][next_tile_col] == -1:
                            print("Nouveau voisin %s %s" % (next_tile_row, next_tile_col))
                            tempMap[next_tile_row][next_tile_col] = biome
                            batchSize -= 1
                            tilesRepartition[biome] -= 1
                            numRetries = 40
                            batchElements.append((next_tile_row, next_tile_col))
                            tilesLeft.remove((next_tile_row, next_tile_col))
                        else:
                            numRetries -= 1

        print(tilesRepartition)

        out = ""
        for row_index, row in tempMap.items():
            out += '\n'
            for col_index, col in row.items():
                out += str(col) + " "
                self._map.append(Case(col, (row_index, col_index)))

        print(out)

    def getMap(self):
        return self._map


map = Map()
map.generate_map((10, 10))







