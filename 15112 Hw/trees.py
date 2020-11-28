from cmu_112_graphics import *
import math, copy, projectionOperations 

def appStarted(app):
    app.level = 1

def drawSierpinskiTriangle(app, canvas, level, x, y, size):
    # (x,y) is the lower-left corner of the triangle
    # size is the length of a side
    # Need a bit of trig to calculate the top point
    if level == 0:
        topY = y - (size**2 - (size/2)**2)**0.5
        canvas.create_polygon(x, y, x+size, y, x+size/2, topY, fill='spring green')
    else:
        # Bottom-left triangle
        drawSierpinskiTriangle(app, canvas, level-1, x, y, size/2)
        # Bottom-right triangle
        drawSierpinskiTriangle(app, canvas, level-1, x+size/2, y, size/2)
        # Top triangle
        midY = y - ((size/2)**2 - (size/4)**2)**0.5
        drawSierpinskiTriangle(app, canvas, level-1, x+size/4, midY, size/2)

def keyPressed(app, event):
    if event.key in ['Up', 'Right']:
        app.level += 1
    elif (event.key in ['Down', 'Left']) and (app.level > 0):
        app.level -= 1

def redrawAll(app, canvas):
    margin = min(app.width, app.height)//10
    x, y = margin, app.height-margin
    size = min(app.width, app.height) - 2*margin
    drawSierpinskiTriangle(app, canvas, app.level, x, y, size)
    canvas.create_text(app.width/2, 0,
                       text = f'Level {app.level} Fractal',
                       font = 'Arial ' + str(int(margin/3)) + ' bold',
                       anchor='n')
    canvas.create_text(app.width/2, margin,
                       text = 'Use arrows to change level',
                       font = 'Arial ' + str(int(margin/4)),
                       anchor='s')

runApp(width=400, height=400)