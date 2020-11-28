
from cmu_112_graphics import *
import math, copy, random, projectionOperations

class worldElement(object):
    #each element is a kind of element (tree, dirt, etc) 
    #with their own 4 surrounding points stored in coords
    def __init__(self, coords, time):
        self.coords = coords
        self.timeCreated = time
        self.exists = True
    
    def drawElement(self, canvas, app):
        pt1R, pt1C = self.coords[0]
        pt2R, pt2C = self.coords[1]
        pt3R, pt3C = self.coords[2]
        pt4R, pt4C = self.coords[3]

        pt1 = app.threeDPoints[pt1R][pt1C]
        pt2 = app.threeDPoints[pt2R][pt2C]
        pt3 = app.threeDPoints[pt3R][pt3C]
        pt4 = app.threeDPoints[pt4R][pt4C]

        #get the center point first
        baseX, baseY = projectionOperations.centerOf4Coords(pt1, pt2, pt3,pt4)
        canvas.create_oval(baseX-5, baseY-5, baseX +  5, baseY + 5)

    def checkSurrounding(self, app):
        return 
    
    def checkTime(self, app):
        return

class Rock(worldElement):
    def __init__(self, coords, time):
        super().__init__(coords, time)
    
    def drawElement(self, canvas, app):
        pt1R, pt1C = self.coords[0]
        pt2R, pt2C = self.coords[1]
        pt3R, pt3C = self.coords[2]
        pt4R, pt4C = self.coords[3]

        pt1 = app.threeDPoints[pt1R][pt1C]
        pt2 = app.threeDPoints[pt2R][pt2C]
        pt3 = app.threeDPoints[pt3R][pt3C]
        pt4 = app.threeDPoints[pt4R][pt4C]

        #get the center point first
        baseX, baseY = projectionOperations.centerOf4Coords(pt1, pt2, pt3,pt4)
        canvas.create_oval(baseX-5, baseY-5, baseX +  5, baseY + 5, fill = "gray")

    def checkSurrounding(self, app):
        for lakeCoords in app.lakeRowsAndCols:
            if lakeCoords in self.coords:
                self.exists = False
                dirt = Dirt(self.coords, app.time)
                app.worldElementList.append(dirt)
                app.canDirt = True

class Plant(worldElement): 
    def __init__(self, coords, time):
        super().__init__(coords, time)
        self.length = 10 #change to random later
        self.color = "green"
    '''
    def drawElement(self, canvas, app):
        pt1R, pt1C = self.coords[0]
        pt2R, pt2C = self.coords[1]
        pt3R, pt3C = self.coords[2]
        pt4R, pt4C = self.coords[3]

        pt1 = [pt1R, pt1C, app.boardA[pt1R][pt1C]]
        pt2 = [pt2R, pt1C, app.boardA[pt2R][pt2C]]
        pt3 = [pt3R, pt3C, app.boardA[pt3R][pt3C]]
        pt4 = [pt4R, pt4C, app.boardA[pt4R][pt4C]]
        print(pt1, pt2, pt3, pt4)
        #this is the actual 3D points
        p1, p2 = projectionOperations.orthogonalVector(pt1, pt2, pt3, pt4, self.length)

        #translate to 2D
        x2, y2 = projectionOperations.pointTransformer(pt1)
        x1, y1 = projectionOperations.pointTransformer(pt2)

        canvas.create_line(x1, y1, x2, y2)
    
    def checkSurrounding(self, app):
        for element in app.worldElements:
            if isinstance(element, Rock):
                for point in coords:
                    if point in self.coord
                    self.exists = False
                    dirt = Dirt(self.coords)
                    app.worldElementList.append(dirt)
                    app.canDirt = True
    '''

    def drawElement(self, canvas, app):
        pt1R, pt1C = self.coords[0]
        pt2R, pt2C = self.coords[1]
        pt3R, pt3C = self.coords[2]
        pt4R, pt4C = self.coords[3]

        pt1 = app.threeDPoints[pt1R][pt1C]
        pt2 = app.threeDPoints[pt2R][pt2C]
        pt3 = app.threeDPoints[pt3R][pt3C]
        pt4 = app.threeDPoints[pt4R][pt4C]

        #get the center point first
        baseX, baseY = projectionOperations.centerOf4Coords(pt1, pt2, pt3,pt4)
        canvas.create_oval(baseX-5, baseY-5, baseX +  5, baseY + 5, fill = self.color)

    def checkSurrounding(self, app):
        for element in app.worldElementList:
            if isinstance(element, Dirt):
                for dirtPoint in element.coords:
                    if dirtPoint in self.coords:
                        self.exists = False
                        tree = Tree(self.coords, app.time)
                        app.worldElementList.append(tree)
                        app.canTree = True
                        break
        for element in app.worldElementList:
            if isinstance(element, Rock):
                for rockPoint in element.coords:
                    if rockPoint in self.coords:
                        self.exists = False
                        seed = Seed(self.coords, app.time)
                        app.worldElementList.append(seed)
                        app.canSeed = True
                        break

        for lakeCoords in app.lakeRowsAndCols:
            if lakeCoords in self.coords:
                self.color = "light sea green"

class Dirt(worldElement):
    def __init__(self, coords, time):
        super().__init__(coords, time)
       
    def drawElement(self, canvas, app):
        pt1R, pt1C = self.coords[0]
        pt2R, pt2C = self.coords[1]
        pt3R, pt3C = self.coords[2]
        pt4R, pt4C = self.coords[3]

        pt1 = app.threeDPoints[pt1R][pt1C]
        pt2 = app.threeDPoints[pt2R][pt2C]
        pt3 = app.threeDPoints[pt3R][pt3C]
        pt4 = app.threeDPoints[pt4R][pt4C]

        #get the center point first
        baseX, baseY = projectionOperations.centerOf4Coords(pt1, pt2, pt3,pt4)
        canvas.create_oval(baseX-5, baseY-5, baseX +  5, baseY + 5, fill = "tan")
    
    def checkSurrounding(self, app):
        nearbySeeds = set()

        #making a garden
        for element in app.worldElementList:
            if isinstance(element, Seed):
                for seedPoint in element.coords:
                    if seedPoint in self.coords and element not in nearbySeeds:
                        nearbySeeds.add(element)
                        break
        nearbySeeds = list(nearbySeeds)
        if len(nearbySeeds)>=2:
            for i in range(len(nearbySeeds)-1):
                app.worldElementList.remove(nearbySeeds[i])
            seed = Seed(self.coords, app.time, True)
            app.worldElementList.append(seed)
                        

class Tree(worldElement):
    def __init__(self, coords, time):
        super().__init__(coords, time)
        self.spawnedAnimal = False
        
    def drawElement(self, canvas, app):
        pt1R, pt1C = self.coords[0]
        pt2R, pt2C = self.coords[1]
        pt3R, pt3C = self.coords[2]
        pt4R, pt4C = self.coords[3]

        pt1 = app.threeDPoints[pt1R][pt1C]
        pt2 = app.threeDPoints[pt2R][pt2C]
        pt3 = app.threeDPoints[pt3R][pt3C]
        pt4 = app.threeDPoints[pt4R][pt4C]

        #get the center point first
        baseX, baseY = projectionOperations.centerOf4Coords(pt1, pt2, pt3,pt4)
        canvas.create_oval(baseX-5, baseY-10, baseX +  5, baseY + 5, fill = "dark green")
   
    def checkTime(self, app): 
        if (app.time - self.timeCreated > 2) and not self.spawnedAnimal:
            num = random.randrange(1, 4, 1)
            animal = None
            if num == 1:
                animal = Rabbit(self.coords, app.time)
            elif num == 2:
                animal = Cow(self.coords, app.time)
            elif num == 3:
                animal = Bird(self.coords, app.time)
            app.worldElementList.append(animal)
            self.spawnedAnimal = True

class Rabbit(worldElement):
    def __init__(self, coords, time):
        super().__init__(coords, time)
       
    def drawElement(self, canvas, app):
        pt1R, pt1C = self.coords[0]
        pt2R, pt2C = self.coords[1]
        pt3R, pt3C = self.coords[2]
        pt4R, pt4C = self.coords[3]

        pt1 = app.threeDPoints[pt1R][pt1C]
        pt2 = app.threeDPoints[pt2R][pt2C]
        pt3 = app.threeDPoints[pt3R][pt3C]
        pt4 = app.threeDPoints[pt4R][pt4C]

        #get the center point first
        baseX, baseY = projectionOperations.centerOf4Coords(pt1, pt2, pt3,pt4)
        canvas.create_oval(baseX-5, baseY-5, baseX +  5, baseY + 5, fill = "white")
        canvas.create_oval(baseX-2, baseY-10, baseX, baseY + 1, fill = "white")
        canvas.create_oval(baseX, baseY-10, baseX+2, baseY + 1, fill = "white")

class Bird(worldElement):
    def __init__(self, coords, time):
        super().__init__(coords, time)
       
    def drawElement(self, canvas, app):
        pt1R, pt1C = self.coords[0]
        pt2R, pt2C = self.coords[1]
        pt3R, pt3C = self.coords[2]
        pt4R, pt4C = self.coords[3]

        pt1 = app.threeDPoints[pt1R][pt1C]
        pt2 = app.threeDPoints[pt2R][pt2C]
        pt3 = app.threeDPoints[pt3R][pt3C]
        pt4 = app.threeDPoints[pt4R][pt4C]

        #get the center point first
        baseX, baseY = projectionOperations.centerOf4Coords(pt1, pt2, pt3,pt4)
        canvas.create_oval(baseX-5, baseY-5, baseX +  5, baseY + 5, fill = "orange")
        canvas.create_oval(baseX-2, baseY-10, baseX, baseY + 1, fill = "orange")
        canvas.create_oval(baseX, baseY-10, baseX+2, baseY + 1, fill = "orange")

class Cow(worldElement):
    def __init__(self, coords, time):
        super().__init__(coords, time)
       
    def drawElement(self, canvas, app):
        pt1R, pt1C = self.coords[0]
        pt2R, pt2C = self.coords[1]
        pt3R, pt3C = self.coords[2]
        pt4R, pt4C = self.coords[3]

        pt1 = app.threeDPoints[pt1R][pt1C]
        pt2 = app.threeDPoints[pt2R][pt2C]
        pt3 = app.threeDPoints[pt3R][pt3C]
        pt4 = app.threeDPoints[pt4R][pt4C]

        #get the center point first
        baseX, baseY = projectionOperations.centerOf4Coords(pt1, pt2, pt3,pt4)
        canvas.create_oval(baseX-5, baseY-5, baseX +  5, baseY + 5, fill = "gainsboro")

class Seed(worldElement):
    def __init__(self, coords, time, gardenStatus = False):
        super().__init__(coords, time)
        self.inGarden = gardenStatus
        
    def drawElement(self, canvas, app):
        pt1R, pt1C = self.coords[0]
        pt2R, pt2C = self.coords[1]
        pt3R, pt3C = self.coords[2]
        pt4R, pt4C = self.coords[3]

        pt1 = app.threeDPoints[pt1R][pt1C]
        pt2 = app.threeDPoints[pt2R][pt2C]
        pt3 = app.threeDPoints[pt3R][pt3C]
        pt4 = app.threeDPoints[pt4R][pt4C]

        #get the center point first
        baseX, baseY = projectionOperations.centerOf4Coords(pt1, pt2, pt3,pt4)
        canvas.create_oval(baseX-2, baseY-2, baseX+2, baseY+2, fill = "red")
        base2X, base2Y = baseX-2, baseY-4
        canvas.create_oval(base2X-2, base2Y-2, base2X+2, base2Y+2, fill = "tomato2")
        base3X, base3Y = baseX+1, baseY+1
        canvas.create_oval(base2X-2, base2Y-2, base2X+2, base2Y+2, fill = "OrangeRed3")

    def checkTime(self, app): 
        if (app.time - self.timeCreated > 2) and self.inGarden: 
            flower = Flower(self.coords, app.time)   
            app.worldElementList.append(flower)
            self.exist = False
             
class Flower(worldElement):
    def __init__(self, coords, time):
        super().__init__(coords, time)
        
    def drawElement(self, canvas, app):
        pt1R, pt1C = self.coords[0]
        pt2R, pt2C = self.coords[1]
        pt3R, pt3C = self.coords[2]
        pt4R, pt4C = self.coords[3]

        pt1 = app.threeDPoints[pt1R][pt1C]
        pt2 = app.threeDPoints[pt2R][pt2C]
        pt3 = app.threeDPoints[pt3R][pt3C]
        pt4 = app.threeDPoints[pt4R][pt4C]

        #get the center point first
        baseX, baseY = projectionOperations.centerOf4Coords(pt1, pt2, pt3,pt4)
        canvas.create_oval(baseX-5, baseY-5, baseX+5, baseY+5, fill = "gold")

   