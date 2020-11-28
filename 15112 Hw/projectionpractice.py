import math

#make2dlist
def make2dList(rows, cols):
        return [([0] * cols) for row in range(rows)]

#matrix multiplier
def matrixmultiplication(X, Y):
    if isinstance(Y[0],int): 
        r = len(X) 
        c = 1
        result = make2dList(r, c)

        # iterate through rows of X
        for i in range(len(X)):
            # iterate through columns of Y
            for j in range(1): #range(len(Y[0])):
                # iterate through rows of Y
                for k in range(3):
                    result[i][j] += X[i][k] * Y[k]
        return result
    else:
        r = len(X) 
        c = len(Y[0])
        result = make2dList(r, c)

        # iterate through rows of X
        for i in range(len(X)):
            # iterate through columns of Y
            for j in range(len(Y[0])):
            # iterate through rows of Y
                for k in range(len(Y)): 
                    result[i][j] += X[i][k] * Y[k][j]
        return result

#takes in a (X, Y, Z, 1) point and applies transformation
def pointTransformer(point):
    #set k1 matrix 
    sin = math.cos(math.pi*5/6)
    cos = math.sin(math.pi*5/6)
    k1 = [[cos, -1 * sin , 50], \
        [sin,  cos      , 50], \
        [0  ,  0      , 1] ] 

    #set k2 matrix 
    k2 = [[20,5,0,0], \
        [5,20,0,0], \
        [0,0,1,0] ] 

    k = matrixmultiplication(k1, k2)

    newPoint = matrixmultiplication(k, point)
    #x translation
    newPoint[0] = newPoint[0][0] + 70
    newPoint[1] = newPoint[1][0] + 380
    return newPoint
    
#pt1 is the < minX
#pt2 is the ^ minY
#pt3 is the > maxX
#pt4 is the v maxY
#takes in 4 x,y coordinates and generates the middle of them
def centerOf4Coords(pt1, pt2, pt3, pt4):
    minX = min(pt1[0], pt2[0])
    minY = max(pt2[1], pt3[1])

    maxX = max(pt3[0], pt4[0])
    maxY = min(pt1[1], pt4[1])

    baseX = (minX + maxX)/2
    baseY = (minY + maxY)/2

    return baseX, baseY

#takes in 4 3D coordinates, x,y,z and calculates the center
def centerOf4Coords(pt1, pt2, pt3, pt4):
    minX = min(pt1[0], pt2[0])
    minY = max(pt2[1], pt3[1])

    maxX = max(pt3[0], pt4[0])
    maxY = min(pt1[1], pt4[1])

    #get the center point first
    baseX = (minX + maxX)/2
    baseY = (minY + maxY)/2

    return baseX, baseY

   
#returns pt1, pt2 vector orthogonal to the center of the grid 
def orthogonalNormalVector(pt1, pt2, pt3,pt4):
    baseX, baseY = centerOf4Coords(pt1, pt2, pt3,pt4)
    #get the plane
    u, v = planeFrom3Dpoints(pt1, pt2, pt3, pt4)
    print(u)
    print(v)
    #equation = (u[2]*v[3]−v[2]*u[3])x−(u[1]v[3]−v[1]u[3])j+(u[1]v[2]−v[1]u[2])k.
    a = u[1]*v[2]-v[1]*u[2]
    b = (-1*u[0]*v[2])+v[0]*u[2]
    c = u[0]*v[1]-v[0]*u[1]
    magnitude = magnitudeOfVector([a,b,c])

#calculate magnitude of vector, any dimension works
def magnitudeOfVector(v):
    sum = 0
    for component in v:
        sum += component**2
    return math.sqrt(sum)

#takes in 3D data
def planeFrom3Dpoints(pt1, pt2, pt3,pt4):
    #make matrix out of the points that spans their plane
    
    v1 = [pt2[0]-pt1[0], pt2[1]-pt1[1], pt2[2]-pt1[2]]
    v2 = [pt4[0]-pt3[0], pt4[1]-pt3[1], pt4[2]-pt3[2]]

    return [v1, v2]


def insidePolygon(p1,p2,p3,p4, target):
    if insideTriangle(p1,p2,p3, target) \
        or insideTriangle(p1,p3,p4, target):
        return True

def insideTriangle(p1,p2,p3, target):
    # compute vectors        
    v0 = [0,0]
    v1 = [0,0]
    v2 = [0,0]
    
    v0[0] = p3[0] - p1[0]
    v0[1] = p3[1] - p1[1]

    v1[0] = p2[0] - p1[0]
    v1[1] = p2[1] - p1[1]

    v2[0] = target[0] - p1[0]
    v2[1] = target[1] - p1[1]

    # Compute dot products
    dot00 = dotProduct(v0, v0)
    dot01 = dotProduct(v0, v1)
    dot02 = dotProduct(v0, v2)
    dot11 = dotProduct(v1, v1)
    dot12 = dotProduct(v1, v2)

    invDenom = (dot00 * dot11 - dot01 * dot01)
    if invDenom == 0:
        invDenom = 100000000000
    else:
        invDenom = 1/invDenom
    u = (dot11 * dot02 - dot01 * dot12) * invDenom
    v = (dot00 * dot12 - dot01 * dot02) * invDenom

    # Check if target point is in triangle
    return (u >= 0) and (v >= 0) and (u + v < 1)

def dotProduct(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1]

print(magnitudeOfVector([-5, 1, -7]))