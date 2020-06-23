import random
import numpy as np

class Structure:
    def __init__(self, pointMap,pos):
        self.pos = pos
        if self.convexShapeTest(pointMap):
            self.shape = pointMap
        else:
            self.shape = [(0,0),(0,10),(10,10),(10,10)]

        self.radius = np.sqrt(pow(max(self.shape)[0], 2) + pow(max(self.shape)[1], 2))
        for i in range(len(self.pointMap)):
            self.pointMap[i][0] += self.pos[0]
            self.pointMap[i][1] += self.pos[1]

    def generateConvexStructure(self, edges,size):
        #generate random sample of x and y´s
        pointmap = []
        lx = [random.randrange(0, size, 0.5) for _ in range(edges)]
        ly = [random.randrange(0, size, 0.5) for _ in range(edges)]

        #sort x list and y list
        lx.sort()
        ly.sort()

        #take the largest element and smallest.
        mxX = lx.pop(0)
        miX = lx.pop(edges)

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
        miY = ly.pop(edges)

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
            vec.append({"angle":np.arctan(y,x), "pos":(x,y)})

        #sort by angle
        vec = sorted(vec,key=lambda i: i['angle'])

        #append the points to point map and connect end to end
        x, y = 0, 0
        minP = (0,0)
        for v in vec:
            pointmap.append((x,y))
            x += v[0]
            y += v[1]
            minP = min(minP,(x,y))
        # todo eventuall shift if needed

        return pointmap

    def convexShapeTest(self,pointmap):
        if pointmap is None:
            return False
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
                    return False

        return True