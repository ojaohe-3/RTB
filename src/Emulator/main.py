from activity import Activity
from actor import Actor
from structure import Structure
from timewrapper import TimeWrapper
from map import Map
from functools import wraps


sendData =''
workers = []
trucks =[]
activites = []
structures = []
map = Map()

def main():
    print ("generating senario from config file")
    conf = {}
    activites = conf["activites"]
    workers = conf["workers"]
    trucks = conf["trucks"]
    strutures = conf["structures"]


def connectionSetup():
    return
def sendData():
    msg = ''
    if 'not setup' == 'setup':
        connectionSetup()
    return 'completed '+msg

def collisionDetection(func):
    @wraps(func)
    def wrapper(boundBox,vel):
        bounds = []
        for point in boundBox:
            bounds.append(point)
        #create local copy
        mapbound= map.shape
        #test for map shape


        #all placed structures
        for structure in structures:
            #extract shape of each indivudual structure
            shape1 = structure.pointMap
            P = []
            #test for collision of object
            for i in range(0,len(bounds)):
                point1 = bounds[i]
                x1 = point1[0]
                y1 = point1[1]

                point2 = bounds[(i+1)%len(bounds)]
                x2 = point2[0]
                y2 = point2[1]

                #projection vector, normal between 2 points in the shape
                P.append( [-(y2-y1), (x2-x1)])

        #test for activity collision
        boundBox = bounds
        return func(boundBox, vel)
    return wrapper