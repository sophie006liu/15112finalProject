import heapq
import random
import math

#mostly self written, turned to help from https://www.geeksforgeeks.org/a-search-algorithm/
#and https://en.wikipedia.org/wiki/A*_search_algorithm
#and https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
class CoordItem:
    def __init__(self, coord, f,g, parent=None):
        self.coord = coord
        self.f = f
        self.g = g
        self.parent = parent

    def __repr__(self):
        return f"{self.coord}"

    def __lt__ (self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __eq__(self, other):
        return self.f == other.f


directions = [(-1, -1), (-1, 0), (-1, 1),
    (0, -1),         (0, 1),
    (1, -1), (1, 0), (1, 1) ]
    
#make2dlist taken from class
def make2dList(rows, cols, defVal = 0.0):
        return [([defVal] * cols) for row in range(rows)]

def build_path(coordItem):
    path = []
    cur = coordItem
    while cur is not None:
        path.append(cur.coord)
        cur = cur.parent
    return path[::-1]

def aStarSearch(selfCoord, targetCoord, grid):
    # 1Initialize the open list all the available options
    start = CoordItem(selfCoord, 0, 0, None)
    openList = []
    heapq.heapify(openList)
    heapq.heappush(openList, start)
    closedDict = {}
    openDict = {}
    path = {}
    while len(openList) > 0: 
        coordItem= heapq.heappop(openList)
        closedDict[coordItem.coord] = coordItem.f 

        for direction in directions: 
            newRow = coordItem.coord[0] + direction[0]
            newCol = coordItem.coord[1] + direction[1] 
            if (newRow >= len(grid)) or newCol >= len(grid[0]):
                continue

            if grid[newRow][newCol] == 1:  # the cell is blocked
                closedDict[(newRow, newCol)] = 100000000
                continue

            if targetCoord[0] == newRow and targetCoord[1] == newCol:
                return build_path(coordItem)
        
            g = coordItem.g = round(math.sqrt((direction[0])**2 + (direction[1])**2), 5)
            h = round(math.sqrt((newRow-targetCoord[0])**2 + (newCol-targetCoord[1])**2), 5)
            f = g + h
            succ = CoordItem((newRow,newCol), f, g, coordItem)
            if (newRow,newCol) in openDict and openDict[(newRow,newCol)] < f:
                continue
            elif (newRow,newCol) in closedDict and closedDict[(newRow,newCol)] < f:
                continue
            else:
                heapq.heappush(openList, succ)
    return []

def makeRandom2dList(rows, cols, defVal = 0.0):
    return [([0] * cols) for row in range(rows)]
    
def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows, cols = len(a), len(a[0])
    fieldWidth = maxItemLength(a)
    print('[')
    for row in range(rows):
        print(' [ ', end='')
        for col in range(cols):
            if (col > 0): print(', ', end='')
            print(str(a[row][col]).rjust(fieldWidth), end='')
        print(' ]')
    print(']')



def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

grid = makeRandom2dList(10,10)
grid[1][1] = 1
grid[2][2] = 1
path = aStarSearch((0,0), (9,9), grid)
print2dList(grid)
print(path)