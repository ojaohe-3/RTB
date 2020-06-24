import random
import time
from src.Emulator.activity import Activity
import numpy as np
class Actor:
    def __init__(self,initPos,type,vel,shape,name):
        self.pos = initPos
        self.vel = vel
        self.status = "disabled"
        self.type = type
        self.name = name
        self.activity = None
        self.shape = shape
        self.radius = np.sqrt(pow(max(shape)[0],2)+pow(max(shape)[1],2))
        for i in range(len(shape)):
            self.shape[i][0] += self.pos[0]
            self.shape[i][1] += self.pos[1]
    #Move towards a pos
    def updatePos(self,npos):
        x = npos[0] - self.pos[0]
        y = npos[1] - self.pos[1]
        if(x == 0):
            return # is at destination.
        theta = np.arctan(y/x)
        #generate velocity vector
        dx = self.vel*np.cos(theta)
        dy = self.vel*np.sin(theta)

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

    def setActivity(self,n_activity):
        self.activity = n_activity

    def setDestination(self, point):
        self.activity = Activity(point,"moving", "unscheduled", time.time+random.randrange(10,100))


    def toJson(self):
        return self.name