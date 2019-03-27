
import numpy

from settings.enums import BiomesTypes
from settings import biomeSettings
from settings import settings
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
        self._dictMap = {}
        self._height = size[0]
        self._width = size[1]
        self._player = None
        self._exit = None
        self._monsters = []

    def generate(self):
        self._generateMap()
        self._generatePlayerAndExit()

    def inMap(self, position):
        return 1 <= position[0] <= self._height and 1 <= position[1] <= self._width

    def walkable(self, position):
        return self._dictMap[position[0]][position[1]].isWalkable();

    def getNeighbors(self, position, isGeneration=False):
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

        neighborsList = list(filter(self.inMap, neighborsList))

        if not isGeneration:
            neighborsList = list(filter(self.walkable, neighborsList))

        return neighborsList

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
        if pos[0] in self._dictMap and pos[1] in self._dictMap[pos[1]]:
            return self. _dictMap[pos[0]][pos[1]]
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

                visited = False

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        visited = True
                        break

                # We found we already checked this
                if visited:
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

    # Retourne les cases visibles autour de center avec une certaine
    # portée de vision
    def getVisibleCases(self, center, range):
        results = []

        # Récupère tous les candidats
        spiral_ring = self.getCaseSpiralRing(center, range)

        for case in spiral_ring:
            # Récupère la ligne directe
            line = self.getLineBetweenCases(center, case)

            # Si il n'y a pas de case bloquant la vision (i.e. montagne)
            # dans la ligne, on ajoute la case
            if not any(case_inline.getType() == BiomesTypes.MOUNTAIN for case_inline in line):
                results.append(case)

        return results

    def getLineBetweenCases(self, case1, case2):
        cube1 = utils.oddQToCube(case1.getPosition()[0], case1.getPosition()[1])
        cube2 = utils.oddQToCube(case2.getPosition()[0], case2.getPosition()[1])

        # Récupère une ligne de triplets de cube
        cube_line = utils.cubeLineDraw(cube1[0], cube1[1], cube1[2], cube2[0], cube2[1], cube2[2])

        line = []
        for cube in cube_line:
            case = self.getCaseAtPos(utils.cubeToOddQ(cube[0], cube[1], cube[2]))

            # Si la case est dans la carte
            if case is not None:
                line.append(case)

        return line


    def _generatePlayerAndExit(self):
        while True:
            self._player = self._cases[numpy.random.randint(0, len(self._cases))]
            self._exit = self._cases[numpy.random.randint(0, len(self._cases))]

            if len(self.getShortestPath(self._player.getPosition(), self._exit.getPosition())) >= settings.MAP_MIN_DIST_PLAYER_EXIT:
                break

        print("Pos player %s" % str(self._player.getPosition()))
        print("Pos exit %s" % str(self._exit.getPosition()))

    def _generateMonsters(self):
        for i in range(0, settings.MONSTERS_NUM):
            while True:
                randomTile = self._cases[numpy.random.randint(0, len(self._cases))]

                if randomTile != self._player and randomTile != self._exit \
                        and randomTile not in self._monsters \
                        and len(self.getShortestPath(self._player.getPosition(),
                            self._exit.getPosition())) >= settings.MIN_DIST_PLAYER_MONSTERS:
                    self._monsters.append(randomTile)
                    break

        print(self._monsters)


    def _generateObjects(self):
        print("Not implmented")

    def _generateMap(self):
        totalTiles = self._height * self._width
        tilesRepartition = {}
        tilesLeft = []

        # Init map
        print("Taille totale %s" % totalTiles)
        for i in range(1, self._height + 1):
            self._dictMap.update({i: {}})
            for j in range(1, self._width + 1):
                self._dictMap[i].update({j: Case(-1, (i, j))})
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
                case = self._dictMap[row_index][col_index]
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
                        neighbors = self.getNeighbors(batchElements[randomTileFromBatch].getPosition(), True)
                        randomNextTile = numpy.random.randint(0, len(neighbors))
                        nextTile = neighbors[randomNextTile]
                        next_tile_row = nextTile[0]
                        next_tile_col = nextTile[1]

                        if self._dictMap[next_tile_row][next_tile_col].getType() == -1:
                            print("Nouveau voisin %s %s" % (next_tile_row, next_tile_col))
                            self._dictMap[next_tile_row][next_tile_col].setType(biome)
                            batchSize -= 1
                            tilesRepartition[biome] -= 1
                            numRetries = 40
                            batchElements.append(self._dictMap[next_tile_row][next_tile_col])
                            tilesLeft.remove((next_tile_row, next_tile_col))
                        else:
                            numRetries -= 1

        print(tilesRepartition)

        out = ""
        for row_index, row in self._dictMap.items():
            out += '\n'
            for col_index, col in row.items():
                out += str(col) + " "
                self._cases.append(col)

        print(out)

    def getCases(self):
        return self._cases
