import random
import time
import Activity
class Actor:
    def __init__(self,initPos,type):
        self.pos = initPos
        self.vel = 0 #always in rest
        self.status = "inactive"
        self.type = type
        self.activity = None

    def setActivity(self,n_activity):
        self.activity = n_activity
    def setDestination(self, point):
<<<<<<< Updated upstream
        self.activity = Activity(point,"moving", "unschedual", time.time+random.randrange(10,100))
=======
        self.activity = Activity(point,"moving", "unscheduled", time.time+random.randrange(10,100))


    def toJson(self):
        json_msg = {
            "name": self.name,
            "position": self.pos
        }
        return json_msg
>>>>>>> Stashed changes
