from cmu_112_graphics import * #graphics package taken from class
import math, copy, random, projectionOperationsWithDrag, worldElements, BoidTest 
#from 15112 class website https://www.cs.cmu.edu/~112/notes/notes-graphics.html

def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def drawBackGround(canvas, app):
    r = 1
    b = 2*math.pi/600
    time = 50*math.cos(b*app.time)+50
    g = int(2.18804*time)
    b = int(2.18804*time + 35.15009)
    color = rgbString(r,g,b)
    canvas.create_rectangle(0,0, app.width, app.height, fill = color)
    if app.time != 0 and (app.time-200)%600 < 150: 
        drawStars(canvas, app)

def drawStars(canvas, app):
    for star in app.stars:
        x, y= star[0], star[1]
        size = random.randrange(7, 21, 1)
        pixel = size/7
        hx1, hx2, hy1, hy2 = x-(size/2), x+(size/2), y-(pixel/2), y+(pixel/2)
        sx1, sx2, sy1, sy2 = x-(pixel*3/2), x+(pixel*3/2), y-(pixel*3/2), y+(pixel*3/2)
        vx1 = x-(pixel/2)
        vx2 = x+(pixel/2)
        vy1 = y-(pixel*9/2)
        vy2 = y+(pixel*9/2)
        canvas.create_rectangle(hx1, hy1, hx2, hy2, fill = "white", width = 0)
        canvas.create_rectangle(sx1, sy1, sx2, sy2, fill = "white", width = 0)
        canvas.create_rectangle(vx1, vy1, vx2, vy2, fill = "white", width = 0) 

class Cloud(object):
    def __init__(self, x, y, size, color, smallSize, midSize):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.smallSize = smallSize
        self.midSize = midSize

    def drawCloud(self, canvas, app):
        #Big rect
        x, y = self.x, self.y
        size, smallSize, midSize = self.size, self.smallSize, self.midSize

        bx2, by2 = x+size, y+size
        #little left rectangle
        sx1, sy1 = x-smallSize, y+size-smallSize
        sx2, sy2 = x, by2
        #middle sized right rectangle
        mx1, my1 = bx2, y+size-midSize
        mx2, my2 = bx2+midSize, by2
        canvas.create_rectangle(x, y, bx2, by2, fill = self.color, width = 0)
        canvas.create_rectangle(sx1, sy1, sx2, sy2, fill = self.color, width = 0)
        canvas.create_rectangle(mx1, my1, mx2, my2, fill = self.color, width = 0) 




    