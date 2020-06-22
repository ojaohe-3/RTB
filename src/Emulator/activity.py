import time

import numpy as np


class Activity:
    def __init__(self,pos,type,status,stime):
        self.stime = stime
        self.pos = pos
        self.bounds = [(0,0),(1,0),(1,1),(0,1)]
        for i in range(0,len(self.bouds)):
            self.bounds[i][0] += self.pos[0]
            self.bounds[i][1] += self.pos[1]
        self.type = type
        self. status = status
        self.radius = np.sqrt(max(self.bounds)[0] **2 + max(self.bounds)[1]**2)
    def isActive(self):
        if self.stime-time.time() < 0:
            if "active" in self.status:
                return True
        return False

