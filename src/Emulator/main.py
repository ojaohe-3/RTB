from RTB.src.Emulator.activity import Activity
from RTB.src.Emulator.actor import Actor
from RTB.src.Emulator.structure import Structure
from RTB.src.Emulator.timewrapper import TimeWrapper
from RTB.src.Emulator.map import Map
from functools import wraps


sendData =''
workers = []
trucks =[]
activites = []
structures = []
actors = []
map = Map()
conf = {}

def moveActorTowards(actor, pos):
    actor.updatePos(pos)
    hit, obj = checkForCollisions(actor)
    if(hit):
        #todo if this does return an delta vector, that is the required difference to displace the shapes, then translate to point.
        #not to mention all the errors in the universe
        displacement = checkCollisionDisplacment(obj,actor.bounds)
        actor.setPos(displacement)

def main():

    activites = conf["activites"]
    workers = conf["workers"]
    trucks = conf["trucks"]
    strutures = conf["structures"]
    actors = workers+trucks
    #todo asyncio implementation, main loop should sleep every itteration to give space for connection and sending data
    while(True):
        #main loop
        #move actors
        for a in actors:
            moveActorTowards(a, a.activity.pos)
        #todo sample data
        #todo send sample data

def connectionSetup():
    #todo setup connection
    return

def sendData(data):
    #todo send data
    return

def checkForCollisions(actor):
    mapbound= map.shape
    #inside of map
    if(not checkCollision(mapbound,actor.bounds)):
        print("out of bounds")
        return False, mapbound
    #all placed structures
    for structure in structures:
        shape1 = structure.pointMap
        if checkCollision(shape1,actor.bounds):
            print("collision detected")
            return True, shape1
    #all placed activites
    for activity in activites:
        if activity.isActive():
            shape1 = activity.bounds
            if (checkCollision(shape1, actor.bounds)):
                print("actor arrived at a activity")
                activity.status = 'completed'
                #todo make event

                return True, shape1
    #other actors, if we care to
    # for a in actors:
    #     if(a != actor):
    #         if(checkCollision(a.bounds,actor.bounds)):
    #             return True, a.bounds

    return False, None
def checkCollision(shape1,shape2):
    s1 = shape1
    s2 = shape2

    for shape in range(0,2):
        #reverse the entire process to project onto the normal of the inital projection vector
        if shape == 1:
            s1 = shape2
            s2 = shape1
        for i in range(0, len(s2)):
            point1 = s2[i]
            x1 = point1[0]
            y1 = point1[1]

            point2 = s2[(i + 1) % len(s2)]
            x2 = point2[0]
            y2 = point2[1]

            # A projected vector, normal between 2 points in the shape that collision will be projected against
            P = (-(y2 - y1), (x2 - x1))

            max1 = -9999999
            min1 = 9999999
            # discover the maximum length of any projected line of the shape on projection vector P
            for j in range(0, len(s2)):
                point = s2[j]
                x = point[0]
                y = point[1]
                Q = P[0] * x + P[1] * y
                max1 = max(max, Q)
                min1 = min(min, Q)

            # project against the other shape and take the maximum length of a line
            max2 = -9999999
            min2 = 9999999
            for k in range(0, len(s1)):
                point = s1[k]
                x = point[0]
                y = point[1]
                Q = P[0] * x + P[1] * y
                max2 = max(max, Q)
                min2 = min(min, Q)

            # if any of the shapes orthogonal projected vector where to not intersect with the other shapes projection, then there cannot be any collision

            if not (max2 >= min1 and max1 >= min2):
                return False
    return True


def checkCollisionDisplacment(shape1,shape2):
    s1 = shape1
    s2 = shape2
    dx = 0
    dy = 0
    for shape in range(0,2):
        #reverse the entire process to project onto the normal of the inital projection vector
        if shape == 1:
            s1 = shape2
            s2 = shape1

        pos = findCentroid(s2)
        for p in s1:
            for i in range(0, len(s2)):
                qs = s2[i]
                qe = s2[(i+1)%len(s2)]
                #i dunno man, line segment algoritm, or something
                h = (qe[0]-qs[0])*(pos[1]-p[1])-(qe[1]-qs[1])*(pos[0]-p[0])
                t1 = ((qs[1]-qe[1])*(pos[0]-qs[0])+(qs[0]-qe[0])*(pos[1]-qs[1]))/h
                t2 = ((pos[1]-p[1])*(pos[0]-qs[0])+(pos[1]-p[1])*(pos[1]-qs[1]))/h

                #collision detected condition
                if t1 >= 0 and t1 < 1 and t2 >= 0 and t2 < 1:
                    #The second shape to our reference need to be subtracted to the final displacement
                    if shape == 0:
                        dx += (1-t1)*(p[0]-pos[0])
                        dy += (1-t1)*(p[1]-pos[1])
                    else:
                        dx -= (1 - t1) * (p[0] - pos[0])
                        dy -= (1 - t1) * (p[1] - pos[1])

    return (dx,dy)

# credit https://progr.interplanety.org/en/python-how-to-find-the-polygon-center-coordinates/
def findCentroid(self,vertexes):
    x = [vertex[0] for vertex in vertexes]
    y = [vertex[1] for vertex in vertexes]
    length = len(vertexes)
    x0 = sum(x) / length
    y0 = sum(y) / length
    return (x0, y0)