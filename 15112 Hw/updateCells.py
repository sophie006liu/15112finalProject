from cmu_112_graphics import *
import math, copy, projectionOperations, worldElements  


def appStarted(app):
    app.drawLine = False
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()

    app.boardA = make2dList(app.rows, app.cols) 
    app.threeDPoints = make2dList(app.rows, app.cols)

    if not app.drawLine:
        app.timerDelay = 50
    else:
        app.timerDelay = 1000

    app.count = 0
    app.dA = 0.2
    app.dA_diagonal = 0.05

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

    app.time = 0
#make2dlist
def make2dList(rows, cols):
        return [([0] * cols) for row in range(rows)]

def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

def mousePressed(app, event):
    if not app.drawLine:
        #if the user clicks then they drop a seed into the diffusing board
        rows = event.y // app.cellSize
        cols = event.x // app.cellSize
        app.boardA[rows][cols] = app.rows

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
    if event.key == "g" and not app.drawLine:
        transformPoints(app)
        app.drawLine = True
    
    if event.key == "r" or event.key == "p":
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

    elif event.key == "s":
        if not app.canSeed:
            print("Seeds isn't in the recipe book! Get creative lmao")
        else:
            app.mode = "s"

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
#let the cells diffuse
def updateCells(app):
    newBoardA = make2dList(app.rows, app.cols)  
    for row in range(app.rows):
        for col in range(app.cols):
            newNeighbor = 0 
            if row == 0:
                if col == 0:  
                    right = app.dA * app.boardA[row][col + 1]
                    downRight = app.dA_diagonal * app.boardA[row + 1][col + 1]
                    down = app.dA * app.boardA[row + 1][col]
                    
                    newNeighbor = right + downRight + down
 
                elif col == app.cols - 1:
                    left = app.dA * app.boardA[row][col - 1]
                    downLeft = app.dA_diagonal * app.boardA[row + 1][col - 1]
                    down = app.dA * app.boardA[row + 1][col]  
                    
                    newNeighbor = left + downLeft + down
 
                else:
                    right = app.dA * app.boardA[row][col + 1]
                    downRight = app.dA_diagonal * app.boardA[row + 1][col + 1]
                    left = app.dA * app.boardA[row][col - 1]
                    downLeft = app.dA_diagonal * app.boardA[row + 1][col - 1]
                    down = app.dA * app.boardA[row + 1][col]         

                    newNeighbor = right + downRight + left + downLeft + down 

            elif col == 0:
                if row == app.rows - 1:
                    right = app.dA * app.boardA[row][col + 1]
                    upRight = app.dA_diagonal * app.boardA[row - 1][col + 1]
                    up = app.dA * app.boardA[row - 1][col] 

                    newNeighbor = right + upRight + up
 
                elif row > 0:
                    right = app.dA * app.boardA[row][col + 1]
                    upRight = app.dA_diagonal * app.boardA[row - 1][col + 1]
                    up = app.dA * app.boardA[row - 1][col] 
                    down = app.dA * app.boardA[row + 1][col]                   
                    downRight = app.dA_diagonal * app.boardA[row + 1][col + 1]

                    newNeighbor = right + upRight + up + down +downRight
 
            elif row == app.rows - 1:
                if col == app.cols - 1:
                    left = app.dA * app.boardA[row][col - 1]
                    up = app.dA * app.boardA[row - 1][col]
                    upLeft = app.dA_diagonal * app.boardA[row - 1][col - 1]

                    newNeighbor = left + up + upLeft 
                elif col > 0:
                    right = app.dA * app.boardA[row][col + 1]
                    upRight = app.dA_diagonal * app.boardA[row - 1][col + 1]   
                    up = app.dA * app.boardA[row - 1][col]   
                    left = app.dA * app.boardA[row][col - 1]       
                    upLeft = app.dA_diagonal * app.boardA[row - 1][col - 1]   

                    newNeighbor = right + upRight + up + left + upLeft  
  
            elif col == app.cols - 1:
                if row < app.rows -1 and row > 0:
                    up = app.dA * app.boardA[row - 1][col] 
                    down = app.dA * app.boardA[row + 1][col]                   
                    left = app.dA * app.boardA[row][col - 1]
                    downLeft = app.dA_diagonal * app.boardA[row + 1][col - 1]
                    upLeft = app.dA_diagonal * app.boardA[row - 1][col - 1] 

                    newNeighbor = up + down + left + downLeft + upLeft

            else:
                right = app.dA * app.boardA[row][col + 1]
                upRight = app.dA_diagonal * app.boardA[row - 1][col + 1]
                downRight = app.dA_diagonal * app.boardA[row + 1][col + 1]
                up = app.dA * app.boardA[row - 1][col] 
                down = app.dA * app.boardA[row + 1][col]                   
                left = app.dA * app.boardA[row][col - 1]
                downLeft = app.dA_diagonal * app.boardA[row + 1][col - 1]
                upLeft = app.dA_diagonal * app.boardA[row - 1][col - 1] 

                newNeighbor = right + upRight + downRight + up + down + left + \
                    downLeft + upLeft        

            ogA = app.boardA[row][col]   
            newBoardA[row][col] = newNeighbor 

    app.boardA = newBoardA    

#setting up the diffuse board dimensions
def gameDimensions():
    rows = 21
    cols = 21
    cellSize = 40
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
                text = str(round(app.boardA[row][col], 2))
                if (app.boardA[row][col]) != 0:
                    scaleRed = int(math.log(app.boardA[row][col])) * 4 + 126
                else:
                    scaleRed = 1
                scaleGreen = 255 -scaleRed
                color = rgbString(scaleRed, scaleGreen, 0)
                x0, y0, x1, y1 = getCellBounds(app, row, col)
                canvas.create_rectangle(x0,y0, x1, y1, fill = color)
                canvas.create_text((x0+x1)/2, (y0+y1)/2, text = text, \
                    font = "arial 6")
    else:
        #draw the contour plot
        drawLine(canvas, app)
        
        #draw all elements
        for index, element in enumerate(app.worldElementList):
            element.drawElement(canvas, app) #the coordinates are 4 sets of row and col

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
            startPoint = (i, j, app.boardA[i][j], 1) 
            newPoint = projectionOperations.pointTransformer(startPoint)
            if (app.boardA[i][j] > 0.12):
                app.lakeRowsAndCols.append([i,j])
            app.threeDPoints[i][j] = newPoint

#constantly gets called
def timerFired(app):
    if not app.drawLine:
        updateCells(app)

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
