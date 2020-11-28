from cmu_112_graphics import *

def appStarted(app):
    app.level = 1
    app.r = 100
def drawFreddy(app, canvas, level, x, y, r):
    if level == 0:
        canvas.create_oval(x+r, y +r, x-r, y-r, fill = 'maroon', outline = 'black')
    else:
        x1 = y/2
        y1 = y/2
        newR = r/2
        drawFreddy(app, canvas, level -1, x1, y1, newR)

        x2 = x + x1

        drawFreddy(app, canvas, level - 1, x2, y1, newR)

def keyPressed(app, event):
    if event.key in ['Up', 'Right']:
            app.level += 1
    elif (event.key in ['Down', 'Left']) and(app.level > 0):
            app.level -= 1
    
def redrawAll(app, canvas):
    drawFreddy(app, canvas, app.level, app.width/2, app.height/2 , app.r)


runApp(width = 400, height = 400)