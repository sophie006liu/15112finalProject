import turtle

def appStarted():
    screen = turtle.Screen()
    winTop = screen.window_height()//2
    drawText('Turtle Puzzle 1', 0, winTop - 40)
    drawText('Click the mouse!', 0, winTop - 65, size=20)
    drawText('Gold dots in top and bottom, navy dots on the sides',
             0, winTop - 90, size=20)
    turtle.pensize(8)

