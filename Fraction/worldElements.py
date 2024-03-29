
from cmu_112_graphics import *
import math, copy, random, projectionOperations

class worldElement(object):
    #each element is a kind of element (tree, dirt, etc) 
    #with their own 4 surrounding points stored in coords
    def __init__(self, coords, time):
        self.coords = coords
        self.timeCreated = time
    
    def drawElement(self, canvas, app):
        pt1R, pt1C = self.coords[0]
        pt2R, pt2C = self.coords[1]
        pt3R, pt3C = self.coords[2]
        pt4R, pt4C = self.coords[3]

        #get points that outline the grid containg the world element
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
        #if the rock is submerged in water you get dirt   
        for lakeCoords in app.lakeRowsAndCols:
            if lakeCoords in self.coords:
                app.worldElementList.remove(self)
                dirt = Dirt(self.coords, app.time)
                app.worldElementList.append(dirt)
                app.canDirt = True
                break
        
        #if there are 2 trees nearby fire is created!
        nearbyTrees = set()
        for element in app.worldElementList:
            if isinstance(element, Tree):
                for treePoint in element.coords:
                    if treePoint in self.coords and element not in nearbyTrees:
                        nearbyTrees.add(element)
                        break

        nearbyTrees = list(nearbyTrees)
        if len(nearbyTrees)>=2:
            for i in range(2):
                app.worldElementList.remove(nearbyTrees[i])
            fire = Fire(self.coords, app.time)
            app.worldElementList.append(fire)

class Fire(worldElement):
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
        canvas.create_rectangle(baseX-5, baseY-2, baseX+5, baseY+2, fill = "red")

    def checkSurrounding(self, app):
        #fire and rock creates steel
        for element in app.worldElementList:
            if isinstance(element, Rock):
                if element.coords == self.coords:
                    continue
                else:
                    for rockPoint in element.coords:
                        if rockPoint in self.coords: 
                            steel = Steel(self.coords, app.time)
                            app.worldElementList.append(steel)
                            app.canSteel = True
                            break

class Steel(worldElement):
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
        canvas.create_rectangle(baseX-5, baseY-2, baseX+5, baseY+2, fill = "LightBlue3")

    def checkSurrounding(self, app):
        #steel near trees becomes a tool
        for element in app.worldElementList:
            if isinstance(element, Tree): 
                    for treePoint in element.coords:
                        if treePoint in self.coords: 
                            tool = Tool(self.coords, app.time)
                            app.worldElementList.append(tool)
                            app.canTool = True
                            break

class Tool(worldElement):
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
        canvas.create_rectangle(baseX-5, baseY-2, baseX+5, baseY+2, fill = "SlateBlue2")
    
    #tool near rock makes iron, coal, diamond, or gold
    def checkSurrounding(self, app):
        for element in app.worldElementList:
            if isinstance(element, Rock): 
                for rockPoint in element.coords:
                    if rockPoint in self.coords: 
                        num = random.randrange(1, 20, 1)
                        ore = None
                        if num >= 1 and num < 10:
                            ore = Iron(element.coords, app.time)
                            app.canIron = True
                        elif num >= 10 and num < 18:
                            ore = Coal(element.coords, app.time)
                            app.canCoal = True
                        elif num == 18:
                            ore = Diamond(element.coords, app.time)
                            app.canDiamond = True
                        elif num ==19:
                            ore = Gold(element.coords, app.time)
                            app.canGold = True
                        app.worldElementList.remove(element) 
                        if ore == None:
                            print("did not generate ore, ", num)
                        app.worldElementList.append(ore)
                        break

class Coal(worldElement):
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
        canvas.create_oval(baseX-3, baseY-2, baseX+3, baseY+2, fill = "black")

class Iron(worldElement):
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
        canvas.create_rectangle(baseX-3, baseY-2, baseX+3, baseY+2, fill = "LavenderBlush2")
    
    #iron and rock makes lantern
    def checkSurrounding(self, app):
        for element in app.worldElementList:
            if isinstance(element, Coal): 
                for rockPoint in element.coords:
                    if rockPoint in self.coords: 
                        lantern = Lantern(element.coords, app.time)
                        app.worldElementList.append(lantern)
                        app.worldElementList.remove(element)
                        app.canLantern = True
                        break

class Lantern(worldElement):
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
        canvas.create_rectangle(baseX-5, baseY-5, baseX+5, baseY+5, fill = "goldenrod1")

class Diamond(worldElement):
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
        canvas.create_rectangle(baseX-2, baseY-2, baseX+2, baseY+2, fill = "cyan")

class Gold(worldElement):
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
        canvas.create_rectangle(baseX-2, baseY-2, baseX+2, baseY+2, fill = "goldenrod1")

class Plant(worldElement): 
    def __init__(self, coords, time):
        super().__init__(coords, time)
        self.length = 10 #change to random later
        self.color = "green"

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

    #plant grows into tree
    def checkSurrounding(self, app):
        for element in app.worldElementList:
            if isinstance(element, Dirt):
                for dirtPoint in element.coords:
                    if dirtPoint in self.coords:
                        app.worldElementList.remove(self)
                        tree = Tree(self.coords, app.time)
                        app.worldElementList.append(tree)
                        app.canTree = True
                        break

        #plant submerged in water becomes seaweed
        for lakeCoords in app.lakeRowsAndCols:
            if lakeCoords in self.coords:
                self.color = "light sea green"
        
    def checkTime(self, app): 
        if (app.time - self.timeCreated > 2) and self.color == "light sea green" and app.canTool: 
            fish = Fish(self.coords, app.time)
            app.worldElementList.append(fish)

class Fish(worldElement):
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
        canvas.create_rectangle(baseX-5, baseY-2, baseX+5, baseY+2, fill = "salmon")
    
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
            for i in range(2):
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
        #over time the tree will spawn an animal
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
            flower = Flower(self.coords, app.time, True)   
            app.worldElementList.append(flower)
            app.canFlower = True
            app.worldElementList.remove(self)
    
             
class Flower(worldElement):
    def __init__(self, coords, time, inGardenStatus = False):
        super().__init__(coords, time)
        self.inGarden = inGardenStatus
        
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

    def checkTime(self, app): 
        if (app.time - self.timeCreated > 2) and self.inGarden: 
            fruit = Fruit(self.coords, app.time, True)   
            app.worldElementList.append(fruit)
            app.canFruit = True
            app.worldElementList.remove(self)

class Fruit(worldElement):
    def __init__(self, coords, time, inGardenStatus = False):
        super().__init__(coords, time)
        self.inGarden = inGardenStatus
        
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
        canvas.create_oval(baseX-5, baseY-5, baseX+5, baseY+5, fill = "orchid1")

