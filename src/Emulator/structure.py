import random
import numpy as np

from src.Emulator.site_object import SiteObject


class Structure(SiteObject):


    def __init__(self, pos, name):
        shape = self.generateConvexStructure(int(random.randrange(3, 12)),random.random() * 10+5)
        super().__init__(pos, shape, name)


    def generateConvexStructure(self, edges,size):
        #generate random sample of x and y´s
        pointmap = []
        lx = [random.random()*size for _ in range(edges)]
        ly = [random.random()*size for _ in range(edges)]

        #sort x list and y list
        lx.sort()
        ly.sort()

        #take the largest element and smallest. (first and end)
        mxX = lx.pop(0)
        miX = lx.pop(-1)

        #chain them, and connect them
        lastTop = miX
        lastBottom = miX
        vx = []
        for x in lx:
            if bool(random.getrandbits(1)):
                vx.append(x-lastTop)
                lastTop = x
            else:
                vx.append(lastBottom - x)
                lastBottom = x
        vx.append(mxX-lastTop)
        vx.append(lastBottom - mxX)

        #do the same for y axis
        mxY = ly.pop(0)
        miY = ly.pop(-1) 

        lastTop = miY
        lastBottom = miY
        vy = []

        for y in lx:
            if bool(random.getrandbits(1)):
                vy.append(y - lastTop)
                lastTop = y
            else:
                vy.append(lastBottom - y)
                lastBottom = y
        vy.append(mxY - lastTop)
        vy.append(lastBottom - mxY)

        #shuffle both vector lists
        random.shuffle(vx)
        random.shuffle(vy)

        #generate a vector list with each point, append value of angle and position
        vec = []
        for i in range(edges):
            x = vx[i]
            y = vy[i]
            vec.append({"angle": np.arctan(y/x), "pos": [x, y]})

        #sort by angle
        vec = sorted(vec,key=lambda i: i['angle'])

        #append the points to point map and connect end to end
        x, y = 0.0, 0.0
        minP = [0,0]
        for v in vec:
            pointmap.append([x,y])
            x += v["pos"][0]
            y += v["pos"][1]
            minP = min(minP,[x,y])
        # todo eventuall shift if needed

        return pointmap
#depricated
    # def convexShapeTest(self,pointmap):
    #     if pointmap is None:
    #         return False
    #     else:
    #         #for every vector of a shape in a point map, the angle between them must be less than 90 degrees
    #         for i in range(0,len(pointmap)):
    #             point = pointmap[i]
    #             x1 = point[0]
    #             y1 = point[1]
    #
    #             point[(i+1)%len(pointmap)]
    #             x2 = point[0]
    #             y2 = point[0]
    #             x = x2-x1
    #             y = y2 - y1
    #
    #             if np.abs(np.arctan(y/x)) > np.pie/2 :
    #                 return False
    #
    #     return True