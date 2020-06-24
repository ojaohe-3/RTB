import time

import numpy as np


class Activity:
    def __init__(self,pos,type,status,stime):
        self.stime = stime
        self.pos = pos
        self.shape = [[-3.0,-3.0],[3.0,-3.0],[3.0,3.0],[-3.0,3.0]]
        for i in range(4):
            self.shape[i][0] += self.pos[0]
            self.shape[i][1] += self.pos[1]
        self.type = type
        self.status = status
        self.radius = np.sqrt(max(self.shape)[0] **2 + max(self.shape)[1]**2)

    def isActive(self):
        if self.stime-time.time() < 0:
            if "active" in self.status:
                return True
        return False

