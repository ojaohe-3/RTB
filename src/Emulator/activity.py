import numpy as np

from src.Emulator.site_object import SiteObject


class Activity(SiteObject):
    def __init__(self, pos, type, status, start_time, end_time, index):
        super().__init__(pos, [[-3.0, -3.0], [3.0, -3.0], [3.0, 3.0], [-3.0, 3.0]], "Activity_srn:" + str(index))
        self.end_time = end_time
        self.start_time = start_time
        self.type = type
        self.status = status

    def isActive(self, internal_time):
        # only active when within its time
        if internal_time - self.end_time < 0 and self.start_time - internal_time < 0:
            self.status = 'active'
            return True
        return False

    def toJson(self):
        json_msg = {
            "name": self.name,
            "position": self.pos,
            "shape": self.shape,
            "status": self.status
        }
        return json_msg
