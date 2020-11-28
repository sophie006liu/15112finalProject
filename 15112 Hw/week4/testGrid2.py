import cs112_f20_week4_linter
from cmu_112_graphics import *

def appStarted(app):
    app.rows = 10
    app.cols = 10

    app.xMargin = 10
    app.yMargin = 20
    
def getRectangleBounds(app, row, col):
    gridWidth = app.width - (2*app.xMargin)
    gridHeight = app.height - (2*app.yMargin)

    cellHeight = gridHeight / app.rows
    cellWidth = gridWidth / app.cols

    x0 = app.xMargin + (col * cellWidth)
    x1 = app.xMargin + ((col + 1) * cellWidth)
    y0 = app.yMargin + (row * cellHeight)
    y1 = app.yMargin + ((row + 1) * cellHeight)

    return (x0, y0, x1, y1)
def drawGrid(app, canvas):
    for i in range(app.rows):
        for j in range(app.cols):
            x0, y0, x1, y1 = getRectangleBounds(app, i, j)
            canvas.create_rectangle( x0, y0, x1, y1 )
def redrawAll(app, canvas):
    drawGrid(app, canvas)

def main():
    cs112_f20_week4_linter.lint()
    runApp(width=510, height=540)

if __name__ == '__main__':
    main()
