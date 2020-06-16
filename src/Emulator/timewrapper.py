import time

class TimeWrapper:
    def __init__(self,func):
        self.timeStart = time.time()
        self.func = func

    def __call__(self, *args):
        runtime = time.time()
        self.func(*args)
        endtime = time.time()-runtime
        self.printToLog(self, runtime - self.timeStart, endtime, self.func.__name__)

    def printToLog(self, timeEntry, time,name):
        print(time.clock()+': Function ' +name+ 'at runtime'+str(timeEntry)+' ran in :'+str(time+'s'))

