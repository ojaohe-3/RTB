import random
import numpy as np

from src.Emulator.site_object import SiteObject


class Structure(SiteObject):

    def __init__(self, pos, name):
        shape = self.generateConvexStructure(int(random.randrange(3, 12)), random.random() * 100 + 15)
        super().__init__(pos, shape, name)

    # Pavel Valtr. “Probability that an
    # random points are in convex position.” Discrete & Computational Geometry 13.1 (1995): 637-643.
    def generateConvexStructure(self, edges, size):
        # generate random sample of x and y´s
        pointmap = []
        lx = [random.random() * size for _ in range(edges)]
        ly = [random.random() * size for _ in range(edges)]

        lx.sort()
        ly.sort()

        max_x, max_y = lx.pop(-1), ly.pop(-1)
        min_x, min_y = lx.pop(0), ly.pop(0)
        vx, vy = [], []
        x1, x2, y1, y2 = min_x, min_x, min_y, min_y

        for i in range(len(lx)):
            _x, _y = lx[i], ly[i]
            if (bool(random.getrandbits(1))):
                vx.append(x1 - _x)
                vy.append(y1 - _y)
                x1, y1 = _x, _y
            else:
                vx.append(_x - x1)
                vy.append(_y - y1)
                x2, y2 = _x, _y
        vx.append(x1 - max_x)
        vx.append(max_x - x2)

        vy.append(y1-max_y)
        vy.append(max_y-y1)

        random.shuffle(vx)
        random.shuffle(vy)

        vex = [{'ang': np.arctan(y/x), "position": [x, y]} for x, y in zip(vx, vy)]
        vex = sorted(vex, key=lambda i: i['ang'], reverse=True)
        pointmap = []
        x,y = 0,0
        minPol = 0
        for pos in vex:
            pointmap.append([x,y])
            x, y = x+pos[0], y+pos[1]
            minPol = min(minPol,pos)
        shift = [min_x-minPol[0],min_y-minPol[1]]
        
        return pointmap
# depricated
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
