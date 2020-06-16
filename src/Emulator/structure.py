class Structure:
    def __init__(self, pointMap):
        self.points = pointMap
        self.shape = self.boundsToShape()

    def isInside(self, point):
        return 0

    def boundsToShape(self):
        #do somethings
        return self.pointMap
