import time

import numpy as np

from src.Emulator.site_object import SiteObject


class Activity(SiteObject):
    def __init__(self, pos, _type, status, stime):
        super(pos, [[-3.0, -3.0], [3.0, -3.0], [3.0, 3.0], [-3.0, 3.0]], "Activity_srn:" + hash(str(pos)))
        self.stime = stime
        self.type = _type
        self.status = status

    def isActive(self):
        if self.stime - time.time() < 0:
            if "active" in self.status:
                return True
        return False
