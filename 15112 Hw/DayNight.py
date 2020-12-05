from cmu_112_graphics import * #graphics package taken from class
import math, copy, random, projectionOperations, worldElements, BoidTest#, StarShower don't need this yet/it can't work lol
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
    drawStars(canvas, app)

def drawStars(canvas, app):
    numberStars = random.randrange(20, 40, 1)
    for i in range(numberStars):
        x = random.randrange(7, app.width, 7)
        y = random.randrange(7, app.height, 7)
        size = random.randrange(7, 21, 1)
        pixel = size/7
        hx1, hx2, hy1, hy2 = x-(size/2), x+(size/2), y-(pixel/2), y+(pixel/2)
        sx1, sx2, sy1, sy2 = x-(pixel*3/2), x+(pixel*3/2), y-(pixel*3/2), y+(pixel*3/2)
        vx1 = x-(pixel/2)
        vx2 = x+(pixel/2)
        vy1 = y-(pixel*9/2)
        vy2 = y+(pixel*9/2)
        canvas.create_rectangle(hx1, hy1, hx2, hy2, fill = "white")
        canvas.create_rectangle(sx1, sy1, sx2, sy2, fill = "white")
        canvas.create_rectangle(vx1, vy1, vx2, vy2, fill = "white") 