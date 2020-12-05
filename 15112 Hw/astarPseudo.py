// A* Search Algorithm

#make2dlist taken from class
def make2dList(rows, cols, defVal = 0.0):
        return [([defVal] * cols) for row in range(rows)]

def aStarSearch(selfCoord, targetCoord, path):
    # 1Initialize the open list all the available options

    openList = set() #all the explored ones
    for lowLeftR in len(app.threeDPoints):
        for lowLeftC in range(len(app.threeDPoints[0])-1):
            coord = (lowLeftR, lowLeftC)
            openList.add()

    #2.  Initialize the closed list # put the starting node on the open 
        # list (you can leave its f at zero)
    closedList = set() #explored
    closedList.add(selfCoord)
    openList.remove(selfCoord)

    #3.  while the open list is not empty
    while len(openList) != 0:
        # a) find the node with the least f on the open list, call it "q"
        directions = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),         (0, 1),
                    (1, -1), (1, 0), (1, 1) ]
        scoresTables = make2dList(len(app.threeDPoints), len(app.threeDPoints[0])-1)
        g = round(math.sqrt((row-sRow)**2 + (col-sCol)**2),2)
        f = round(math.sqrt((row-tRow)**2 + (col-tCol)**2),2)
        t = g + f
        scoresTables[newRow][newCol] = (g,f,t)  
        minTScore = scores_Tables[sRow[sCol]
        
        for direction in directions: 
            dRow = direction[0]
            dCol = direction[1]
            newRow = r + dRow
            newCol = c + dCol  
            g = round(math.sqrt((row-sRow)**2 + (col-sCol)**2),2)
            f = round(math.sqrt((row-tRow)**2 + (col-tCol)**2),2)
            t = g + f
            scoresTables[newRow][newCol] = (g,f,t)

                        
        #b) pop q off the open list
        for
        c) generate q's 8 successors and set their 
        parents to q
    
        d) for each successor
            i) if successor is the goal, stop search
            successor.g = q.g + distance between 
                                successor and q
            successor.h = distance from goal to 
            successor (This can be done using many 
            ways, we will discuss three heuristics- 
            Manhattan, Diagonal and Euclidean 
            Heuristics)
            
            successor.f = successor.g + successor.h

            ii) if a node with the same position as 
                successor is in the OPEN list which has a 
            lower f than successor, skip this successor

            iii) if a node with the same position as 
                successor  is in the CLOSED list which has
                a lower f than successor, skip this successor
                otherwise, add  the node to the open list
        end (for loop)
    
        e) push q on the closed list
        end (while loop)