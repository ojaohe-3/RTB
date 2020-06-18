import random
import numpy as np

class Structure:
    def __init__(self, pointMap):
        if self.convexShapeTest(pointMap):
            self.shape = pointMap
        else:
            self.shape = self.generateConvexStructure(random.randrange(0,8), 10*random.random())

    def generateConvexStructure(self, edges,size):
        return [[0,0]]

    def convexShapeTest(self,pointmap):
        if pointmap is None:
            return 0
        else:
            #for every vector of a shape in a point map, the angle between them must be less than 90 degrees
            for i in range(0,len(pointmap)):
                point = pointmap[i]
                x1 = point[0]
                y1 = point[1]

                point[(i+1)%len(pointmap)]
                x2 = point[0]
                y2 = point[0]
                x = x2-x1
                y = y2 - y1

                if np.abs(np.arctan(y/x)) > np.pie/2 :
                    return 0

        return 1