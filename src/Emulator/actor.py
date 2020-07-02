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
        # attributes are not set Until schedual is generated for entire program
        self.activity = None
        self.activities = []
        self.start_time = time.time()

    # Move towards a pos
    def updatePos(self, npos):
        x = npos[0] - self.pos[0]
        y = npos[1] - self.pos[1]
        magnitude = np.sqrt(x ** 2 + y ** 2)

        if (x == 0):
            return  # is at destination.
        # generate velocity vector
        dx = self.vel * x / magnitude
        dy = self.vel * y / magnitude

        self.pos[0] += dx
        self.pos[1] += dy
        # print(f"{self.name} moved to point {str(self.pos)}")
        for i in range(len(self.shape)):
            self.shape[i][0] += dx
            self.shape[i][1] += dy

    # blink to a pos
    def setPos(self, pos):
        self.pos = pos
        for i in range(0, len(self.shape)):
            self.shape[i][0] += pos[0]
            self.shape[i][1] += pos[1]

    def setSchedule(self, life_time, nr_activites):
        self.activities = []
        self.start_time = time.time()
        st_time = self.start_time
        end_time = self.start_time + (life_time / (nr_activites+1)) * random.random()
        for i in range(nr_activites):
            self.activities.append(Activity([random.randrange(0, 600), random.randrange(0, 600)], "Work",
                                            "rest", st_time, end_time, i))

            st_time = end_time + random.random() * 100
            end_time = st_time + (life_time / (nr_activites+1)) * random.random()
            if i == nr_activites - 1:
                end_time = life_time

    def setNextActivity(self):
        if self.activities is not None:
            if self.activity is not None:
                if self.activity.end_time - time.time() < 0:
                    self.activity.status = 'complete'
                    self.activity = None
            elif self.activity is None:
                temp = [a for a in self.activities if a.isActive(time.time())]
                self.activity = temp.pop(0) if len(temp) > 0 else None

