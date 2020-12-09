from cmu_112_graphics import * #graphics package taken from class
import math, copy, random, projectionOperationsWithDrag, worldElements, BoidTest, DayNight

#stores app variables
def appStarted(app): 
    app.drawLine = False #dictates whether gray scott phase or world creation phase
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()

    app.boardA = make2dList(app.rows, app.cols, 1.0) #particle concentrations
    app.boardB = make2dList(app.rows, app.cols, 0.0)  
    app.threeDPoints = make2dList(app.rows, app.cols)

    if not app.drawLine:
        app.timerDelay = 1
    else:
        app.timerDelay = 100000

    app.iter = 0
    app.dA = 0.2    #the A diffusion percentage to adjacent cells
    app.dA_diagonal = 0.05  #the A diffusion percentage to diagonal cells
    app.dB = 0.2    #the B diffusion percentage to adjacent cells
    app.dB_diagonal = 0.05  #the A diffusion percentage to diagonal cells
    app.f = 0.055    #feed rate
    app.k = 0.117    #kill rate

    app.worldElementList = [] #stores all elements present on a board
    app.boidList = []

    app.mode = "r" #what element they are currently placing
    app.canDirt = False  #keeps track of all the elements that have been unlocked
    app.canTree = True
    app.canSeed = False
    app.canFlower = False
    app.canFruit = False
    app.canSteel = False
    app.canTool = False
    app.canIron = False
    app.canGold = False
    app.canDiamond = False
    app.canCoal = False
    app.canLantern = False
    app.lakeRowsAndCols = []

    app.time = 0 #keeps track of the world time 
    app.pause = False #for debugging purposes
    app.endX, app.endY = 0,0
    app.startX, app.startY = 0,0
    app.changeX = app.endX - app.startX 
    app.changeY = app.endY - app.startY 
    
    app.stars = []
    app.setStars = False
    app.cloudList = []
    app.cloudStart = 0 
#make2dlist taken from class
def make2dList(rows, cols, defVal = 0.0):
        return [([defVal] * cols) for row in range(rows)]

#part of the gray scott function, initializes 3x3 area with particle B
def seedB(app, r, c):
    #directions list taken from class
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

#helps to move the board
def mouseReleased(app,event): 
    app.endX, app.endY =  event.x, event.y
    if app.endX != app.startX and app.startY != app.endY:
        app.changeX = app.endX - app.startX
        app.changeY = app.endY - app.startY 

def mousePressed(app, event):
    app.startX, app.startY = event.x, event.y 

    if not app.drawLine:
        #if the user clicks then they drop a seed into the diffusing board
        rows = event.y // app.cellSize
        cols = event.x // app.cellSize 
        seedB(app, rows, cols)

    elif app.drawLine: # we are in the mode of adding elements to the board
        coords = (get3DPointsAroundPoint(app, event.x, event.y)) 
        inLake = False
        for lakeCoords in app.lakeRowsAndCols:
            if lakeCoords in coords: 
                inLake = True
                print("clicked ina lake")

        timeCreated = app.time
        if coords != None:
            element = None
            if app.mode == "r": #rock
                element = worldElements.Rock(coords, timeCreated)
            elif app.mode == 'p': #plant
                element = worldElements.Plant(coords, timeCreated)
            elif  app.mode == 'd': #dirt
                element = worldElements.Dirt(coords, timeCreated)
            elif  app.mode == 't' and not inLake: #tree
                element = worldElements.Tree(coords, timeCreated)
            elif  app.mode == 's': #seed
                element = worldElements.Seed(coords, timeCreated)
            elif  app.mode == 'f': #flower
                element = worldElements.Flower(coords, timeCreated)
            elif  app.mode == 'o': #fruit
                element = worldElements.Fruit(coords, timeCreated)
            elif app.mode == 'm': #steel
                element = worldElements.Steel(coords, timeCreated)
            elif app.mode == '0': #tool
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
            if element:
                app.worldElementList.append(element)  
                   
        elif (event.x%28 !=0 or (event.x//28)%2 ==1) and event.y > 570 and event.y < 600:
            buttonNum = event.x//28 
            if buttonNum == 1: app.mode = "r"  

            if buttonNum == 3: app.mode = "p"

            if buttonNum == 5 and app.canDirt: app.mode = "d"

            if buttonNum == 7 and app.canTree: app.mode = "t"

            if buttonNum == 9 and app.canSeed: app.mode = "s"

            if buttonNum == 11 and app.canFlower: app.mode = "f"

            if buttonNum == 13 and app.canFruit: app.mode = "o"
        
            if buttonNum == 15 and app.canSteel: app.mode = "m"  
            
            if buttonNum == 17 and app.canTool: app.mode = "0" 

            if buttonNum == 19 and app.canIron: app.mode = "1"

            if buttonNum == 21 and app.canDiamond: app.mode = "3"

            if buttonNum == 23 and app.canCoal: app.mode = "2" 

            if buttonNum == 25 and app.canGold: app.mode = "4" 

def keyPressed(app, event):
    #pause the diffusion
    if event.key == "p" and not app.drawLine:
        app.pause = not app.pause

    #leave diffusion board go to 3D terrain
    if event.key == "g" and not app.drawLine:
        transformPoints(app)
        app.drawLine = True

    #switch to rock mode and/or plant mode
    if event.key == "r" or (event.key == "p" and app.drawLine):
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

    elif event.key == "s":
        if not app.canSeed:
            print("Seeds isn't in the recipe book! Get creative lmao")
        else:
            app.mode = "s"
    
    elif event.key == "l":
        if not app.canLantern:
            print("Try the ores!")
        else: 
            app.mode = "5"
    
    elif event.key == "." and app.canDiamond:
        app.threeDPoints.append([ projectionOperationsWithDrag.pointTransformer([len(app.threeDPoints), i, 0, 1]) for i in range(len(app.threeDPoints))  ] )
    
#checks to see if a move in a particular direction is still on the board, helps with gray scott
def neighborExists(app, direction, row, col):
    dRow = direction[0]
    dCol = direction[1]

    newRow = row + dRow
    newCol = col + dCol

    if newRow >= 0 and newRow <= (app.rows-1) and newCol >= 0 and newCol <= (app.cols-1):
        return True
    else:
        return False

#function to function gray scott diffusion reaction model, note this is very slow on 50x50+, but yields cooler patterns
def grayScottRD(app):
    deltaBoardA = make2dList(app.rows, app.cols) 
    deltaBoardB = make2dList(app.rows, app.cols) 
    #directions list idea taken from class
    directions = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),         (0, 1),
                   (1, -1), (1, 0), (1, 1) ]

    #DIFFUSION, simulating Laplacian transform
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

    #apply deltaA and deltaB to the current boardA
    DA = 1.0
    DB = 0.5
    DT = 1.0
    epsilon = 0.0000000000001
    for row in range(app.rows):
        for col in range(app.cols):
            A = app.boardA[row][col]
            B = app.boardB[row][col]
            #making sure the new values of A and B are in range ()
            app.boardA[row][col] = min(1.0, max(epsilon, A + (DA*deltaBoardA[row][col] - A*B*B + app.f*(1.0-A)) * DT))
            app.boardB[row][col] = min(1.0, max(epsilon, B + (DB*deltaBoardB[row][col] + A*B*B - (app.k*B)) * DT))
                
            if app.boardA[row][col] < 0 or app.boardA[row][col] >1:
                #this is the gray scott reaction formula taken from https://www.karlsims.com/rd.html
                print("NewA is out of range", row, col, A, B, deltaBoardA[row][col], A*B*B, deltaBoardB[row][col])
                print(app.boardA[row][col])
            if app.boardB[row][col] < 0 or app.boardB[row][col] > 1:
                print("NewB is out of range", row, col, A, B, deltaBoardA[row][col], A*B*B, deltaBoardB[row][col])

#setting up the diffuse board dimensions
def gameDimensions():
    rows = 21
    cols = 21
    cellSize = 40
    margin = 40
    return (rows, cols ,cellSize, margin)

#2D get cell bounds
def getCellBounds(app, row, col):
    x0 = app.cellSize * col
    y0 = app.cellSize * row 
    x1 = app.cellSize * (col + 1)
    y1 = app.cellSize * (row + 1)
    return x0, y0, x1, y1

#given x,y on the window, it will return the points in threeDpoints that surround the click
def get3DPointsAroundPoint(app, x, y):
    for row in range(len(app.threeDPoints)-1):
        for col in range(len(app.threeDPoints[0])-1):                          
            if projectionOperationsWithDrag.insidePolygon(app.threeDPoints[row][col], \
                app.threeDPoints[row+1][col], \
                app.threeDPoints[row+1][col+1], \
                app.threeDPoints[row][col+1], \
                [x,y], app):
                return  [  [row, col],  [row+1, col] ,\
                [row+1,col+1],  [row,col+1] ]

#from 15112 class website https://www.cs.cmu.edu/~112/notes/notes-graphics.html
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

#draws birds that are boids
def drawBoids(app, canvas):
    for boid in app.boidList:
        x = boid.pos[0]
        y = boid.pos[1]
        canvas.create_oval(x -2, y-2, x+2, y+2, fill = "orange")

#draw the buttons
def drawTopButtons(canvas, width, height, number, color, label):
    start = width*(2*(number-1)+1)/30
    end = width*(2*(number))/30
    canvas.create_rectangle(start, height*5/7, end, height*5/7+30, fill= color)
    canvas.create_text(int((start+end)/2), height*5/7+15,  text = label, fill = "white", font="Arial 12 bold")

#creates the grid and the numbers
def drawBoard(app, canvas): 

    if not app.drawLine:
        for row in range(app.rows):
            for col in range(app.cols):
                scaleBlue = min(255, app.boardA[row][col] * 127 + 127)
                scaleGreen = min(255, app.boardB[row][col] * 127 + 127)
                color = rgbString(1, int(scaleGreen), int(scaleBlue))
                x0, y0, x1, y1 = getCellBounds(app, row, col)
                canvas.create_rectangle(x0,y0, x1, y1, fill = color) 
        canvas.create_text(400, 50, text = "Click anywhere to diffuse from there, then press \'g\' to build the rest of your world.")
    else:
        DayNight.drawBackGround(canvas, app)
        if app.cloudStart:
            for cloud in app.cloudList:
                cloud.drawCloud(canvas, app)
        #draw the contour plot
        drawLine(canvas, app)
        drawBoids(app, canvas)
        #draw all elements
        for index, element in enumerate(app.worldElementList):
            element.drawElement(canvas, app) #the coordinates are 4 sets of row and col
       
        #buttons
        drawTopButtons(canvas, app.width, app.height, 1, "gray", "rock (r)") #rock 1
        drawTopButtons(canvas, app.width, app.height, 2, "green", "plant (p)") #plant 3
        if app.canDirt:
            drawTopButtons(canvas, app.width, app.height, 3, "tan", "dirt (d)") #dirt 5
        if app.canTree:
            drawTopButtons(canvas, app.width, app.height, 4, "dark green", "tree (t)") #tree 7
        if app.canSeed:
            drawTopButtons(canvas, app.width, app.height, 5, "red", "seed (s)") #seed 9
        if app.canFlower:   
            drawTopButtons(canvas, app.width, app.height, 6, "gold", "flower (f)") #flower 11 
        if app.canFruit:    
            drawTopButtons(canvas, app.width, app.height, 7, "orchid1", "fruit (o)") #fruit 13  
        if app.canSteel:
            drawTopButtons(canvas, app.width, app.height, 8, "lightblue3", "steel (m)") #steel 15       
        if app.canTool:    
            drawTopButtons(canvas, app.width, app.height, 9, "slateblue2", "tool (0)") #tool 17 
        if app.canIron:
            drawTopButtons(canvas, app.width, app.height, 10, "lavenderblush2", "iron (1)") #iron 19 
        if app.canDiamond:    
            drawTopButtons(canvas, app.width, app.height, 11, "cyan", "diamond (3)") #diamond 21
        if app.canCoal:   
            drawTopButtons(canvas, app.width, app.height, 12, "black", "coal (2)") #coal 23
        if app.canGold:   
            drawTopButtons(canvas, app.width, app.height, 13, "goldenrod1", "gold (4)")  #gold 25 
        canvas.create_text(400, 700, text = "Click the buttons to see what they are, and place various items next to each other to see what you get.", fill = "white")

#checking surroundings, time of all elements, move animals
def checkAllElements(app):
    for element in app.worldElementList:
        element.checkSurrounding(app)
        element.checkTime(app)
        if isinstance(element, worldElements.Rabbit) or isinstance(element, worldElements.Cow) or isinstance(element, worldElements.Dog):
                element.move(app)

#drawing the lines of the contour plot
def drawLine(canvas, app):
    #draw "horizontal" lines through the board
    for i in range(len(app.threeDPoints)):
        for j in range(len(app.threeDPoints[0])-1):
            startPt = app.threeDPoints[i][j]
            x1 = startPt[0]+app.changeX
            y1 = startPt[1]+app.changeY

            nxtPt = app.threeDPoints[i][j + 1]
            x2 = nxtPt[0]+app.changeX
            y2 = nxtPt[1]+app.changeY
            #debugging purposes to get sense of board orientation
            canvas.create_oval(x1-2, y1-2, x1+2, y1+2, fill = "white")
            canvas.create_line(x1,y1,x2,y2)

    #draw "vertical" lines through the board
    for j in range(len(app.threeDPoints[0])):
        for i in range(len(app.threeDPoints)-1):
            startPt = app.threeDPoints[i][j]
            x1 = startPt[0]+app.changeX
            y1 = startPt[1]+app.changeY

            nxtPt = app.threeDPoints[i+1][j]
            x2 = nxtPt[0]+app.changeX
            y2 = nxtPt[1]+app.changeY

            if i < len(app.boardB) and j < len(app.boardB[0])and (app.boardB[i][j] > 0.35):
                canvas.create_oval(x1-2, y1-2, x1+2, y1+2, fill = "dark blue")
            canvas.create_line(x1,y1,x2,y2)
             
#takes one row in the board and generates a line from it's values
def transformPoints(app):
    #going through that row and generating points from it
    for i in range(len(app.boardA)):
        for j in range(len(app.boardA[0])):
            startPoint = [i, j, app.boardB[i][j]/4, 1]
            newPoint = projectionOperationsWithDrag.pointTransformer(startPoint)
            if (app.boardB[i][j] > 0.35): 
                app.lakeRowsAndCols.append([i,j])

            app.threeDPoints[i][j] = newPoint

#if paused, take one step in diffusing
def oneDiffuse(app):
    grayScottRD(app)

#constantly gets called
def timerFired(app):
    if not app.drawLine and not app.pause:
        grayScottRD(app)
        app.iter += 1

    #checking to see if any elements can react with others
    if app.drawLine: 
        checkAllElements(app)
        #move the boids
        for boid in app.boidList:
            boid.move(app)
            boid.wrapAround(app)

    #if it's night, draw some stars
    if app.time != 0 and (app.time-200)%600 < 150:
        if not app.setStars:
            numberStars = random.randrange(20, 40, 1)
            for i in range(numberStars):
                x = random.randrange(7, app.width, 7)
                y = random.randrange(7, app.height, 7)
                tup = (x,y)
                app.stars.append(tup)
            app.setStars = True
    if (app.time-200)%600 >= 150 and app.setStars:
        app.setStars = False
        app.stars = []

    #chance of clouds
    chance = random.randrange(1, 100, 1)
    if chance>= 1 and chance <=20 and app.cloudStart == 0:
        numberClouds = random.randrange(5, 20, 1)
        for i in range(numberClouds):
            x = random.randrange(1, app.width, 1)
            y = random.randrange(1, app.height, 1)

            colors = ["royalBlue4", "dodgerBlue4", "skyblue4"] 
            color = random.choice(colors)
            size = random.randrange(20, 70, 1)
            smallSize = random.randrange(int(size/5), int(size/2), 1)
            midSize = random.randrange(int(size/3), int(size*4/5), 1)
            cloud = DayNight.Cloud(x, y, size, color, smallSize, midSize)
            app.cloudList.append(cloud)
        app.cloudStart = app.time

    if app.time - app.cloudStart > 200:
        app.cloudStart = 0
        app.cloudList = [] 

    app.time += 1 

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
 

if __name__ == '__main__':
    main() 
