import numpy as np


class SiteObject:
    def __init__(self,pos,shape,name):
        self.pos = pos
        self.shape = shape
        self.name = name
        self.radius = np.sqrt(pow(max(self.shape)[0], 2) + pow(max(self.shape)[1], 2))

        for i in range(len(shape)): #align the shape with its pos
            self.shape[i][0] += self.pos[0]
            self.shape[i][1] += self.pos[1]
    def toJson(self):
        json_msg = {
            "name": self.name,
            "position": self.pos,
            "shape": self.shape
        }
        return json_msg