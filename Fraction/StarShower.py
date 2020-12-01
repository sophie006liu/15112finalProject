from cmu_112_graphics import *
import math, copy, projectionOperations 


def drawStarShower(canvas, depth, x, y, size, level):
    if level == depth + 1:
        return
    else: 
        drawStar(canvas, x + size/2, y, size/3)
        buffr = size/2
        drawStarShower(canvas, depth, x + size/4, y+size/2, size, level+1)


def drawStar(canvas, topLeftX, topLeftY, size):
    topPointX, topPointY = topLeftX + size/2, topLeftY
    midLeftX, midLeftY = topLeftX, topLeftY + size/4
    midRightX, midRightY = topLeftX + size, topLeftY + size/4
    botLeftX, botLeftY = topLeftX + size/4, topLeftY + size
    botRightX, botRightY = topLeftX + size*3/4, topLeftY + size 

    canvas.create_line(botLeftX, botLeftY,topPointX, topPointY)
    canvas.create_line(topPointX, topPointY, botRightX, botRightY)
    canvas.create_line(botRightX, botRightY, midLeftX, midLeftY )
    canvas.create_line(midLeftX, midLeftY, midRightX, midRightY) 
    canvas.create_line(midRightX, midRightY, botLeftX, botLeftY) 

