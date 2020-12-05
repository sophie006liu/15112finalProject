import math

#make2dlist taken from class
def make2dList(rows, cols, defVal = 0.0):
        return [([defVal] * cols) for row in range(rows)]



def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

# Because Python prints 2d lists on one row,
# we might want to write our own function
# that prints 2d lists a bit nicer.
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
    

def aStarChase(start, target, h, total_path, app): 
    #(self, target, app):
    # if the target is not at the same place or no target
    #generate all cells f scores and g scores
    #g score is distance from you
    #f score is distance from target
    tRow = target[0]
    tCol = target[1]
    sRow = start[0]
    sCol = start[1]

    scoresTables = make2dList(5, 5)
    for row in range(5):
        for col in range(5):
            g = round(math.sqrt((row-sRow)**2 + (col-sCol)**2),2)
            f = round(math.sqrt((row-tRow)**2 + (col-tCol)**2),2)
            t = g + f
            scoresTables[row][col] = (g,f,t)
    return scoresTables


    directions = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),         (0, 1),
                   (1, -1), (1, 0), (1, 1) ]


    if start == target:
        totalPath.append(start)
        return totalPath
    #     you get to the target:
    #         return the steps
    else:
        minTScore = scores_Tables[sRow[sCol]
        minDirection = []
        for direction in directions:
            if scores_Tables[sRow + direction[0]][sCol[1]] <= minTScore:
                minTScore = scores_Tables[sRow + direction[0]][sCol[1]] 
                minDirection = direction

    #     take step
    #     update scores
    #     see new scores from the step, if one option less than others take that step
    #     until all steps from that node are worse than the first, 
    #         consider a differ first step from the earliest node available
    #         recurse
       
    # else:      
    #     take next step

print2dList(aStarChase([0,0], [4,4]))


#what do you do if you've checked all directions and the space you're in currently has none that work
#go back to the last node that you came from or do you go back to the first one 
#keep a list of the places you can possibility move