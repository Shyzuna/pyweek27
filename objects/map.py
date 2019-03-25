
import numpy

from settings.enums import BiomesTypes
from settings import biomeSettings
from objects.case import Case

class Map:


    def __init__(self, size):
        self._map = []
        self._height = size[0]
        self._width = size[1]

    def generate(self):
        self._generateMap()
        self._generatePlayerAndExit()

    def inMap(self, position):
        (tile_row, tile_col) = position
        return 1 <= tile_row <= self._height and 1 <= tile_col <= self._width

    def getNeighbors(self, position):
        (tile_row, tile_col) = position
        if tile_row % 2 > 0:
            neighborsList = [
                (tile_col+1, tile_row),
                (tile_col+1, tile_row-1),
                (tile_col, tile_row-1),
                (tile_col-1, tile_row-1),
                (tile_col-1, tile_row),
                (tile_col, tile_row+1)]
        else:
            neighborsList = [
                (tile_col+1, tile_row+1),
                (tile_col+1, tile_row),
                (tile_col, tile_row-1),
                (tile_col-1, tile_row),
                (tile_col-1, tile_row+1),
                (tile_col, tile_row+1)]

        return list(filter(self.inMap, neighborsList))

    def findAPath(self, start, end):
        toProcess = [start]
        processed = {}
        path = []

        while len(toProcess) > 0:
            currentNode = toProcess.pop(0)
            for neighbor in self.getNeighbors(currentNode):
                if neighbor not in processed:
                    processed.update({neighbor: 1})
                    path.append(neighbor)
                    if neighbor[0] == end[0] and neighbor[1] == end[1]:
                        return path
                    else:
                        toProcess.append(neighbor)

        return []



    def _generatePlayerAndExit(self):
        print("Not implmented")

    def _generateObjects(self):
        print("Not implmented")

    def _generateMap(self):
        totalTiles = self._height * self._width
        tilesRepartition = {}
        tempMap = {}
        tilesLeft = []

        # Init map
        print("Taille totale %s" % totalTiles)
        for i in range(1, self._height + 1):
            tempMap.update({i: {}})
            for j in range(1, self._width + 1):
                tempMap[i].update({j: Case((i, j), -1)})
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
                case = tempMap[row_index][col_index]
                if case.getType() == -1:
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

                    case.setType(biome)
                    batchElements = [case]
                    batchSize -= 1
                    tilesRepartition[biome] -= 1
                    tilesLeft.remove((row_index, col_index))

                    # Chose neighbor
                    numRetries = 40
                    while batchSize > 0 and numRetries >= 0:
                        randomTileFromBatch = numpy.random.randint(0, len(batchElements))
                        neighbors = self.getNeighbors(batchElements[randomTileFromBatch].getPosition())
                        randomNextTile = numpy.random.randint(0, len(neighbors))
                        nextTile = neighbors[randomNextTile]
                        next_tile_row = nextTile[0]
                        next_tile_col = nextTile[1]

                        if tempMap[next_tile_row][next_tile_col].getType() == -1:
                            print("Nouveau voisin %s %s" % (next_tile_row, next_tile_col))
                            tempMap[next_tile_row][next_tile_col].setType(biome)
                            batchSize -= 1
                            tilesRepartition[biome] -= 1
                            numRetries = 40
                            batchElements.append(tempMap[next_tile_row][next_tile_col])
                            tilesLeft.remove((next_tile_row, next_tile_col))
                        else:
                            numRetries -= 1

        print(tilesRepartition)

        out = ""
        for row_index, row in tempMap.items():
            out += '\n'
            for col_index, col in row.items():
                out += str(col) + " "
                self._map.append(col)

        print(out)

    def getMap(self):
        return self._map






