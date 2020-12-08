from cmu_112_graphics import * #graphics package taken from class
import math, copy, random

def magnitudeOfVector(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

# distance of two biods
def distance(biod1, biod2):
    return math.sqrt((biod1.pos[0]-biod2.pos[0])**2 + (biod1.pos[1]-biod2.pos[1])**2)


class Boid(object):
    
    def __init__(self, x, y):
        self.pos = [x,y]
        self.maxSpeed = 20

        vx = random.randrange(1, 5)
        vy = random.randrange(1, 5)
        self.vel = [vx, vy]

        dvx = random.randrange(2) - 0.5
        dvy = random.randrange(2) - 0.5
        v2 = [dvx/2, dvy/2]
        self.acc = self.vel[0]*v2[0] + self.vel[0]*v2[0]
        self.neighborhood = 50
        self.vel[0] = v2[0]
        self.vel[0] = v2[1]
    
    def move(self, app): 
        # accelerate
        self.vel[0] += self.acc 
        self.vel[1] += self.acc 

        # coherence 1: follow the main direction of neighbor biodes
        coherence = 6
        avg_vec = [0.0,0.0]
        total = 0
        for biod in app.boidList:
            if biod == self:
                pass
            if distance(self, biod) < self.neighborhood:
                avg_vec[0] += biod.vel[0]
                avg_vec[1] += biod.vel[1]
                total += 1

        if total > 0:
            avg_vec[0] /= total
            avg_vec[1] /= total
            norm = magnitudeOfVector(avg_vec)
            self.vel[0] += (avg_vec[0]/norm) * coherence
            self.vel[1] += (avg_vec[1]/norm) * coherence

        # coherence 2: go towards the center point of biodes
        x_sum = 0
        y_sum = 0
        for biod in app.boidList:
            x_sum += biod.pos[0]
            y_sum += biod.pos[1]
        x_arg = x_sum/len(app.boidList)
        y_arg = y_sum/len(app.boidList)
        
        x_diff = x_arg - self.pos[0]
        y_diff = y_arg - self.pos[1]

        mag= magnitudeOfVector([x_diff,y_diff])
        if mag >0:
            self.vel[0] += x_diff/mag * coherence
            self.vel[1] += y_diff/mag * coherence
        
        # seperation: keep some distance
        for biod in app.boidList:
            if biod == self:
                pass
            dist = math.sqrt((biod.pos[0]-self.pos[0])**2 + (biod.pos[1]-self.pos[1])**2)
            if dist < 20:
                dist2 =math.sqrt((biod.pos[0] + biod.vel[0] -self.pos[0] -self.vel[0])**2 + 
                    (biod.pos[1]  + biod.vel[1] -self.pos[1] - self.vel[1])**2)
                if dist2 > dist:
                    pass
                # next distance if change velocity along x coordinate
                x_dist =math.sqrt((biod.pos[0] + biod.vel[0] -self.pos[0] -self.vel[0])**2 + 
                    (biod.pos[1]-self.pos[1])**2)
                # next distance if change velocity along y coordinate
                y_dist = math.sqrt((biod.pos[0] -self.pos[0])**2 + 
                    (biod.pos[1]  + biod.vel[1] -self.pos[1] - self.vel[1])**2)

                if x_dist < y_dist:
                    # reduce vel[0] to keep distance from biod
                    self.reduceVelocity(0)
                    self.increaseVelocity(1)
                else:
                    self.reduceVelocity(1)
                    self.increaseVelocity(0)

    # change direction and reduce speed before collide with border wall
    def wrapAround(self, app):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        leftMargin = 5
        rightMargin = app.width-6
        topMargin = 5
        bottomMargin = app.height-6
        if self.pos[0] >= rightMargin:
            self.pos[0] = rightMargin - 1
            self.vel[0] *= -1
            self.reduceVelocity(1)
        elif self.pos[0] <= leftMargin:
            self.pos[0] = leftMargin + 1
            self.vel[0] *= -1
            self.reduceVelocity(1)
        if self.pos[1] >= bottomMargin:
            self.pos[1] = bottomMargin - 1
            self.vel[1] *= -1
            self.reduceVelocity(0)
        elif self.pos[1] <= topMargin:
            self.pos[1] = topMargin +1
            self.vel[1] *= -1
            self.reduceVelocity(0)
        self.vel[0] = max(-self.maxSpeed, min(self.maxSpeed, self.vel[0] ))
        self.vel[1] = max(-self.maxSpeed, min(self.maxSpeed, self.vel[1] ))

    def reduceVelocity(self, direction):
        self.vel[direction] =  self.vel[direction] * 0.6

    def increaseVelocity(self, direction):
        self.vel[direction] =  self.vel[direction] * 1.2


  
#make2dlist taken from class
def make2dList(rows, cols, defVal = 0.0):
    return [([defVal] * cols) for row in range(rows)]



#refreshes the canvas each time
def redrawAll(canvas, app):
    drawBoids(canvas, app)

def timerFired(app):
    for boid in app.boidList:
        boid.move(app)
        boid.wrapAround(app)

 


