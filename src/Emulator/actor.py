import random
import time
from RTB.src.Emulator.activity import Activity
class Actor:
    def __init__(self,initPos,type,vel,bounds,name):
        self.pos = initPos
        self.vel = vel
        self.status = "inactive"
        self.type = type
        self.name = name
        self.activity = None
        self.bounds = bounds
    #Move towards a pos
    def updatePos(self,npos):
        upos = (0,0)
        upos[0] = (npos[0]-self.pos[0])
        upos[1] = (npos[1]-self.pos[1])

        for i in range(0,len(self.bounds)):
            self.bounds[i][0] += upos[0]
            self.bounds[i][1] += upos[1]
    #blink to a pos
    def setPos(self, pos):
        self.pos = pos
        for i in range(0,len(self.bounds)):
            self.bounds[i][0] += pos[0]
            self.bounds[i][1] += pos[1]

    def setActivity(self,n_activity):
        self.activity = n_activity

    def setDestination(self, point):
        self.activity = Activity(point,"moving", "unschedual", time.time+random.randrange(10,100))


