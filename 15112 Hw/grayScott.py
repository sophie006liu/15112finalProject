from cmu_112_graphics import *
import math, copy, random, projectionOperations, worldElements, StarShower 


def appStarted(app):
    app.drawLine = False
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()

    app.boardA = make2dList(app.rows, app.cols, 1.0)
    app.boardB = make2dList(app.rows, app.cols, 0.0)  
    app.threeDPoints = make2dList(app.rows, app.cols)

    if not app.drawLine:
        app.timerDelay = 1
    else:
        app.timerDelay = 10000

    app.dA = 0.2 #the diffusion percentage times DA
    app.dA_diagonal = 0.05
    app.dB = 0.2 #the diffusion percentage times DB 
    app.dB_diagonal = 0.05
    #feed rate
    app.f = 0.055
    #kill rate
    app.k = 0.117

    app.iter = 0
    #stores building block coordinates in terms of their surrounding points
    app.blockCoords = []
    app.marbleX = None
    app.marbleY = None

    app.worldElementList = []

    app.mode = "r"
    app.canDirt = True
    app.canTree = True
    app.canSeed = True
    app.canFlower = True
    app.canFruit = True
    app.canSteel = True
    app.canTool = True
    app.canIron = True
    app.canGold = True
    app.canDiamond = True
    app.canCoal = True
    app.canLantern = False
    app.lakeRowsAndCols = []

    app.pause = False
#make2dlist
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

def seedB(app, r, c):
    directions = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),         (0, 1),
                   (1, -1), (1, 0), (1, 1) ]
    app.boardB[r][c] = 1
    for row in range(app.rows):
        for col in range(app.cols):
            for direction in directions:
                if neighborExists(app, direction, row, col):
                    dRow = direction[0]
                    dCol = direction[1]
                    newRow = r + dRow
                    newCol = c + dCol
                    app.boardB[newRow][newCol] = 1
                     
def mousePressed(app, event):
    if not app.drawLine:
        #if the user clicks then they drop a seed into the diffusing board
        rows = event.y // app.cellSize
        cols = event.x // app.cellSize 
        seedB(app, rows, cols)

    elif app.drawLine: # we are in the mode of adding elements to the board
        coords = (get3DPointsAroundPoint(app, event.x, event.y)) 
        timeCreated = app.time
        if app.mode == "r": #rock
            element = worldElements.Rock(coords, timeCreated)
        elif app.mode == 'p': #plant
            element = worldElements.Plant(coords, timeCreated)
        elif  app.mode == 'd': #dirt
            element = worldElements.Dirt(coords, timeCreated)
        elif  app.mode == 't': #tree
            element = worldElements.Tree(coords, timeCreated)
        elif  app.mode == 's': #seed
            element = worldElements.Seed(coords, timeCreated)
        elif  app.mode == 'f': #flower
            element = worldElements.Flower(coords, timeCreated)
        elif  app.mode == 'o': #fruit
            element = worldElements.Fruit(coords, timeCreated)
        elif app.mode == 'm': #steel
            element = worldElements.Steel(coords, timeCreated)
        elif app.mode == '0': #iron
            element = worldElements.Tool(coords, timeCreated)
        elif app.mode == '1': #iron
            element = worldElements.Iron(coords, timeCreated)
        elif app.mode == '2': #coal
            element = worldElements.Coal(coords, timeCreated)
        elif app.mode == '3': #diamond
            element = worldElements.Diamond(coords, timeCreated)
        elif app.mode == '4': #gold
            element = worldElements.Gold(coords, timeCreated)
        elif app.mode == '5': #lantern
            element = worldElements.Lantern(coords, timeCreated)
        app.worldElementList.append(element)      

#if they press g, generate 2d line based off of the diffusing board middle row
def keyPressed(app, event):
    if event.key == "p":
        app.pause = not app.pause
    
    if event.key == "s":
        oneDiffuse(app)

    if event.key == "g" and not app.drawLine:
        transformPoints(app)
        app.drawLine = True

    if event.key == "r": #or event.key == "p":
        app.mode = event.key

    elif event.key == "d":
        if not app.canDirt:
            print("Dirt isn't in the recipe book! How is dirt created?")
        else:
            app.mode = "d"

    elif event.key == "t":
        if not app.canTree:
            print("Trees isn't in the recipe book! How are trees grown?")
        else:
            app.mode = "t"
    
    elif event.key == "f":
        if not app.canFlower:
            print("Flowers isn't in the recipe book! How are flowers grown?")
        else:
            app.mode = "f"

    elif event.key == "o":
        if not app.canFruit:
            print("Fruit isn't in the recipe book! Think about your biology class?")
        else:
            app.mode = "o"

    elif event.key == "m":
        if not app.canSteel:
            print("Steel isn't in the recipe book! Brush up on pre historic living!")
        else:
            app.mode = "m"
    elif event.key == "0":
        if not app.canTool:
            print("I will be generous and tell you tool = steel + ...")
        else:
            app.mode = "0"
    elif event.key == "1":
        if not app.canIron:
            print("It's mine time!")
        else:
            app.mode = "1"
    elif event.key == "2":
        if not app.canCoal:
            print("It's mine time!")
        else:
            app.mode = "2"
    elif event.key == "3":
        if not app.canDiamond:
            print("It's mine time!")
        else:
            app.mode = "3"
    elif event.key == "4":
        if not app.canGold:
            print("It's mine time!")
        else:
            app.mode = "4"
    elif event.key == "5":
        if not app.canGold:
            print("First mine, then coal + iron")
        else:
            app.mode = "5"
    '''
    elif event.key == "s":
        if not app.canSeed:
            print("Seeds isn't in the recipe book! Get creative lmao")
        else:
            app.mode = "s"
    '''
#let the cells diffuse

def neighborExists(app, direction, row, col):
    dRow = direction[0]
    dCol = direction[1]

    newRow = row + dRow
    newCol = col + dCol

    if newRow >= 0 and newRow <= (app.rows-1) and newCol >= 0 and newCol <= (app.cols-1):
        return True
    else:
        return False

def grayScottRD(app):
    deltaBoardA = make2dList(app.rows, app.cols) 
    deltaBoardB = make2dList(app.rows, app.cols) 
    directions = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),         (0, 1),
                   (1, -1), (1, 0), (1, 1) ]

    #DIFFUSION
    #contruct deltaA matrix
    for row in range(app.rows):
        for col in range(app.cols):
            for direction in directions:
                if neighborExists(app, direction, row, col):
                    # adjacent
                    if direction in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                        deltaA = app.dA*app.boardA[row][col] #dA = 0.2*0.2
                        deltaB = app.dB*app.boardB[row][col]  
                    # diagonal
                    if direction in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        deltaA = app.dA_diagonal*app.boardA[row][col] 
                        deltaB = app.dB_diagonal*app.boardB[row][col] 
                    # where I put the delta
                    deltaRow, deltaCol = row+direction[0], col+direction[1]
                    deltaBoardA[deltaRow][deltaCol] += deltaA
                    deltaBoardB[deltaRow][deltaCol] += deltaB
                    # subtract from the center
            deltaBoardA[row][col] -= app.boardA[row][col] 
            deltaBoardB[row][col] -= app.boardB[row][col] 

    #apply deltaA to the current boardA
    DA = 1.0
    DB = 0.5
    DT = 1.0
    epsilon = 0.0000000000001
    for row in range(app.rows):
        for col in range(app.cols):
            A = app.boardA[row][col]
            B = app.boardB[row][col]
            #dA= 0.2 * delta**2 * A
            app.boardA[row][col] = min(1.0, max(epsilon, A + (DA*deltaBoardA[row][col] - A*B*B + app.f*(1.0-A)) * DT))
            app.boardB[row][col] = min(1.0, max(epsilon, B + (DB*deltaBoardB[row][col] + A*B*B - (app.k*B)) * DT))
                
            if app.boardA[row][col] < 0 or app.boardA[row][col] >1:
                print("NewA is out of range", row, col, A, B, deltaBoardA[row][col], A*B*B, deltaBoardB[row][col])
                print(app.boardA[row][col])
            if app.boardB[row][col] < 0 or app.boardB[row][col] > 1:
                print("NewB is out of range", row, col, A, B, deltaBoardA[row][col], A*B*B, deltaBoardB[row][col])
                print(app.boardB[row][col])
    #printBoardA(app)

def printBoardA(app):
    print("new board")
    for row in range(app.rows):
        for col in range(app.cols):
            if abs(app.boardA[row][col] -1.0) > 0.0000000000000000001:
                print("A", row, col,app.boardA[row][col])
            if app.boardB[row][col]:
                print("B", row, col,app.boardB[row][col])
    print()

#setting up the diffuse board dimensions
def gameDimensions():
    rows = 75
    cols = 75
    cellSize = 10
    margin = 40
    return (rows, cols ,cellSize, margin)

def getCellBounds(app, row, col):
    x0 = app.cellSize * col
    y0 = app.cellSize * row 
    x1 = app.cellSize * (col + 1)
    y1 = app.cellSize * (row + 1)
    return x0, y0, x1, y1

def getDistance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

#given x,y on the window, it will return the points in threeDpoints that surround the click
def get3DPointsAroundPoint(app, x, y):

    for row in range(len(app.threeDPoints)-1):
        for col in range(len(app.threeDPoints[0])-1):                          
            if projectionOperations.insidePolygon(app.threeDPoints[row][col], \
                app.threeDPoints[row+1][col], \
                app.threeDPoints[row+1][col+1], \
                app.threeDPoints[row][col+1], \
                [x,y]):
                return  [  [row, col],  [row+1, col] ,\
                [row+1,col+1],  [row,col+1] ]

#from 15112 class website https://www.cs.cmu.edu/~112/notes/notes-graphics.html
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

#creates the grid and the numbers
def drawBoard(app, canvas):
    if not app.drawLine:
        for row in range(app.rows):
            for col in range(app.cols):
                #text = str(round(app.boardA[row][col], 3)) + ", " + \
                    #str(round(app.boardB[row][col], 3))
                #if (app.boardA[row][col]) > 0:
                #scaleRed = min(255, app.boardA[row][col]/(app.boardA[row][col]+ app.boardB[row][col]))
                #color = rgbString(int(scaleRed), 127, 127)
                scaleRed = min(255, app.boardA[row][col] * 127 + 127)
                scaleGreen = min(255, app.boardB[row][col] * 127 + 127)
                color = rgbString(int(scaleRed), int(scaleGreen), 0)
                x0, y0, x1, y1 = getCellBounds(app, row, col)
                canvas.create_rectangle(x0,y0, x1, y1, fill = color)
                #canvas.create_text((x0+x1)/2, (y0+y1)/2, text = text, \
                    #font = "arial 10")
    else:
        #draw the contour plot
        drawLine(canvas, app)
        
        #draw all elements
        for index, element in enumerate(app.worldElementList):
            element.drawElement(canvas, app) #the coordinates are 4 sets of row and col
        
        starChance = random.randrange(1, 101, 1)
        if starChance <= 50:
            starX = random.randrange(30, app.width, 1)
            starY = random.randrange(20, app.height/5, 1)
            StarShower.drawStarShower(canvas, 4, starX, starY, 100, 4)
def checkSurroundingOfAllElements(app):
    #checking surroundings of all elements
    for element in app.worldElementList:
            element.checkSurrounding(app)


def checkTimeOfAllElements(app):
    for element in app.worldElementList:
        element.checkTime(app)

def drawLine(canvas, app):
    for i in range(len(app.threeDPoints)):
        for j in range(len(app.threeDPoints[0])-1):
            startPt = app.threeDPoints[i][j]
            x1 = startPt[0]
            y1 = startPt[1]

            nxtPt = app.threeDPoints[i][j + 1]
            x2 = nxtPt[0]
            y2 = nxtPt[1]
            if (i == 0 and j == 0):
                canvas.create_oval(x1-2, y1-2, x1+2, y1+2, fill = "red")
            elif (i == 1 and j == 1):  
                canvas.create_oval(x1-2, y1-2, x1+2, y1+2, fill = "blue")
            else:
                canvas.create_oval(x1-2, y1-2, x1+2, y1+2)

            canvas.create_line(x1,y1,x2,y2)

    
    for j in range(len(app.threeDPoints[0])):
        for i in range(len(app.threeDPoints)-1):
            startPt = app.threeDPoints[i][j]
            x1 = startPt[0]
            y1 = startPt[1]

            nxtPt = app.threeDPoints[i+1][j]
            x2 = nxtPt[0]
            y2 = nxtPt[1]

            if (app.boardA[i][j] > 0.12):
                canvas.create_oval(x1-2, y1-2, x1+2, y1+2, fill = "dark blue")
            canvas.create_line(x1,y1,x2,y2)
             
#takes one row in the board and generates a line from it's values
def transformPoints(app):
    #going through that row and generating points from it
    for i in range(len(app.boardA)):
        for j in range(len(app.boardA[0])):
            startPoint = [i, j, app.boardA[i][j], 1]
            newPoint = projectionOperations.pointTransformer(startPoint)
            if (app.boardA[i][j] > 0.12):
                app.lakeRowsAndCols.append([i,j])
            app.threeDPoints[i][j] = newPoint

def oneDiffuse(app):
    grayScottRD(app)

#constantly gets called
def timerFired(app):
    if not app.drawLine and not app.pause:
        grayScottRD(app)
        app.iter += 1
        if app.iter%50 == 0:
            print("iteration number : ", app.iter)

    if app.drawLine:
        app.time += 1
        checkSurroundingOfAllElements(app)
        checkTimeOfAllElements(app)

#refreshes the canvas each time
def redrawAll(canvas, app):
    drawBoard(canvas, app)

#starts the simulation
def grayScottyBoy():
    rows, cols, cellSize, margin = gameDimensions()
    width = (cols * cellSize) 
    height = (rows * cellSize) 
    runApp(width = width, height = height)
#################################################
# main
#################################################

#also starts the simulation
def main():
    grayScottyBoy()
    master = Tk()

if __name__ == '__main__':
    main()
