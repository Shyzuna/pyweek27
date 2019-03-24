
import numpy

from settings.enums import BiomesTypes
from settings import biomeSettings


class Map:
    TILES_DIRECTION = [
        [[+1, 0], [+1, -1], [0, -1],
         [-1, -1], [-1, 0], [0, +1]],
        [[+1, +1], [+1, 0], [0, -1],
         [-1, 0], [-1, +1], [0, +1]],
    ]

    def __init__(self):
        self._map = {}

    def generate_map(self, mapSize):
        totalTiles = mapSize[0] * mapSize[1]
        tilesRepartition = {}
        undefinedTiles = []

        # Init map
        print("Taille totale %s" % totalTiles)
        for i in range(0, mapSize[0]):
            self._map.update({i: {}})
            for j in range(0, mapSize[1]):
                self._map[i].update({j: -1})
                undefinedTiles.append((i, j))

        # Compute tiles repartition
        for biome in BiomesTypes:
            delta = numpy.random.uniform(-biomeSettings.BIOMES_SETTINGS[biome]['repartition_delta'],
                                         biomeSettings.BIOMES_SETTINGS[biome]['repartition_delta'])
            tilesNum = totalTiles * (biomeSettings.BIOMES_SETTINGS[biome]['repartition'] - delta)
            tilesRepartition.update({biome: int(tilesNum)})

            print("Repartition de %s nombre de tuiles %s avec delta %s" % (biome, int(tilesNum), delta))

        # Fill map
        for row_index, row in self._map.items():
            for col_index, col in row.items():
                if col == -1:
                    print("Case %s %s non traitée" % (row_index, col_index))
                    biome = BiomesTypes(numpy.random.randint(0, len(BiomesTypes)))
                    batchSize = numpy.random.randint(biomeSettings.BIOMES_SETTINGS[biome]['size_range'][0],
                                                     biomeSettings.BIOMES_SETTINGS[biome]['size_range'][1] + 1)

                    if batchSize > tilesRepartition[biome]:
                        batchSize = tilesRepartition[biome]

                    print("Taille du batch %s de type %s" % (batchSize, biome))

                    self._map[row_index][col_index] = biome
                    batchElements = [(row_index, col_index)]
                    batchSize -= 1

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

                            if next_tile_row >= 0 and next_tile_row < mapSize[0] \
                                and next_tile_col >= 0 and next_tile_col < mapSize[1]:
                                break

                        if self._map[next_tile_row][next_tile_col] == -1:
                            self._map[next_tile_row][next_tile_col] = biome
                            batchSize -= 1
                            tilesRepartition[biome] -= -1
                            numRetries = 40
                            batchElements.append((next_tile_row, next_tile_col))
                        else:
                            numRetries -= 1

        print(tilesRepartition)

        out = ""
        for row_index, row in self._map.items():
            out += '\n'
            for col_index, col in row.items():
                out += str(col) + " "

        print(out)

    def getMap(self):
        return self._map

map = Map()
map.generate_map((10, 10))







