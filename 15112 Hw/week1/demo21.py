import turtle

'''
Demos these turtle methods:

turtle.hideturtle()     do not show the turtle

turtle.showturtle()     show the turtle

For more info, check out the Python Turtle Graphics docs here:
https://docs.python.org/3.3/library/turtle.html


def mousePressed(x, y):
    if (x < 0):
        turtle.showturtle()
    else:
        turtle.hideturtle()
'''
def appStarted():
    screen = turtle.Screen()
    winTop = screen.window_height()//2
    drawText('Turtle Tutorial 1', 0, winTop - 40)
    drawText('Show and Hide!', 0, winTop - 65, size=20)
    drawText('Click mouse on left to show turtle, on right to hide it',
             0, winTop - 90, size=20)

############################################
# Simple Turtle Framework
# (ignore code below here)
############################################

import string

def drawText(label, x, y, font='Arial', size=30, style='bold', align='center'):
    oldx, oldy = turtle.position()
    turtle.penup()
    turtle.goto(x, y)
    turtle.write(label, font=(font, size, style), align=align)
    turtle.goto(oldx, oldy)
    turtle.pendown()

def main(winWidth, winHeight, bgColor):
    screen = turtle.Screen()
    turtle.speed(0)
    turtle.setup(width=winWidth, height=winHeight)
    screen.bgcolor(bgColor)
    appStarted()
    turtle.speed(10)
    '''
    def safeCall(fnName, *args):
        if (fnName in globals()):
            globals()[fnName](*args)
    def keyPressedWrapper(key):
        if (len(key) > 1): key = key.capitalize()
        safeCall('keyPressed', key)
    def bindKey(key):
        if (len(key) > 1) or (ord(key) > 32):
            screen.onkey(lambda: keyPressedWrapper(key), key)
    keys = (['Up', 'Down', 'Left', 'Right', 'space', 'Tab', 'Return'] + 
            list(string.ascii_letters + string.digits))
    for key in keys:
        bindKey(key)
    '''
    screen.listen()
    screen.onclick(lambda x, y: safeCall('mousePressed', x, y))
    screen.mainloop()
    
main(800, 600, 'lightgreen')
