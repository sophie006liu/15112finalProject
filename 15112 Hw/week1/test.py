import math

def numberOfPoolBallRows(balls):
    numerator = -1 + math.sqrt(1+8*balls)
    return math.ceil(numerator/2)

print(numberOfPoolBallRows(8))