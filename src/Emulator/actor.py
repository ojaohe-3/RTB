import random
import time
from src.Emulator.activity import Activity
import numpy as np

from src.Emulator.site_object import SiteObject


class Actor(SiteObject):
    def __init__(self, init_pos, _type, vel, shape, name):
        super().__init__(init_pos, shape, name)
        self.vel = vel
        self.status = "active"
        self.type = _type
        self.activity = None

    #Move towards a pos
    def updatePos(self,npos):
        x = npos[0] - self.pos[0]
        y = npos[1] - self.pos[1]
        magnitude = np.sqrt(x**2 + y**2)

        if(x == 0):
            return # is at destination.
        #generate velocity vector
        dx = self.vel*x/magnitude
        dy = self.vel*y/magnitude

        self.pos[0] += dx
        self.pos[1] += dy
        #print(f"{self.name} moved to point {str(self.pos)}")
        for i in range(len(self.shape)):
            self.shape[i][0] += dx
            self.shape[i][1] += dy

    #blink to a pos
    def setPos(self, pos):
        self.pos = pos
        for i in range(0,len(self.shape)):
            self.shape[i][0] += pos[0]
            self.shape[i][1] += pos[1]


