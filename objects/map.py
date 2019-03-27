
import numpy

from settings.enums import BiomesTypes
from settings import biomeSettings
from objects.case import Case
from objects.hex import Hex
from objects.node import Node
from objects.priorityQueue import PriorityQueue
from modules import utils

oddq_directions = [
    # Pour les colonnes paires
    [Hex(0, -1), Hex(+1, -1), Hex(+1, 0),
     Hex(0, +1), Hex(-1, 0), Hex(-1, -1)],
    # Pour les colonnes impaires
    [Hex(0, -1), Hex(+1, 0), Hex(+1, +1),
     Hex(-1, +1), Hex(0, +1), Hex(-1, 0)]
]

class Map:

    def __init__(self, size):
        self._cases = []
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

    def getCaseAtPos(self, pos):
        for case in self.getCases():
            if case.getPosition() == pos:
                return case
        # Not found
        return None

    def getCaseAtPixel(self, point):
        for case in self.getCases():
            if case.checkHover(point):
                return case
        # Not found
        return None

    def getCaseNeighbours(self, case):
        return self.getCaseRing(case, 1)

    def getCaseRing(self, case, radius):
        x, y, z = utils.oddQToCube(case.getHex().getQ(), case.getHex().getR())
        cubeResults = utils.cubeRing(x, y, z, radius)
        results = []
        for cubeResult in cubeResults:
            x, y, z = cubeResult
            for case in self.getCases():
                if utils.cubeToOddQ(x, y, z) == case.getPosition():
                    results.append(case)

        return results

    def getCaseSpiralRing(self, case, radius):
        x, y, z = utils.oddQToCube(case.getHex().getQ(), case.getHex().getR())
        cubeResults = utils.cubeSpiral(x, y, z, radius)
        results = []

        for cubeResult in cubeResults:
            x, y, z = cubeResult
            for case in self.getCases():
                if utils.cubeToOddQ(x, y, z) == case.getPosition():
                    results.append(case)

        return results

    # Renvoie la série de cases constituant le chemin
    # le plus court entre start et end (les deux cases
    # sont incluses dans le chemin)
    # *doit* contourner les montagnes.
    def getShortestPath(self, start, end):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Impossible de compute si les cases de départ ou de fin sont infranchissables
        if self.getCaseAtPos(start).getType() == BiomesTypes.MOUNTAIN or\
                self.getCaseAtPos(end).getType() == BiomesTypes.MOUNTAIN:
            return []

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(self.getCaseAtPos(current.position))
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            if current_node.position[0] % 2 > 0:
                new_hexs = oddq_directions[1]
            else:
                new_hexs = oddq_directions[0]

            for new_hex in new_hexs:  # Adjacent hexs

                # Get node position
                new_position = new_hex.getPosition()
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if not self.inMap(node_position):
                    continue

                # Make sure walkable terrain
                new_case = self.getCaseAtPos(node_position)
                if new_case.getType() == BiomesTypes.MOUNTAIN:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                            (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

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
                tempMap[i].update({j: Case(-1, (i, j))})
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
                self._cases.append(col)

        print(out)

    def getCases(self):
        return self._cases
