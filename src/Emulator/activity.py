import time

import numpy as np

from src.Emulator.site_object import SiteObject


class Activity(SiteObject):
    def __init__(self, pos, type, status, stime, index):
        super().__init__(pos, [[-3.0, -3.0], [3.0, -3.0], [3.0, 3.0], [-3.0, 3.0]], "Activity_srn:" + str(index))
        self.stime = stime
        self.type = type
        self.status = status

    def isActive(self):
        if self.stime - time.time() < 0:
            if "active" in self.status:
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
