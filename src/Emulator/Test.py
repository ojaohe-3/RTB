import random
import unittest
import toml
from Emulator.activity import Activity
from Emulator.actor import Actor
from Emulator.collision import separating_axis_theorem
from Emulator.map import Map
from Emulator.structure import Structure
import time
import pickle

_map = Map()


def generateSim():
    w = []
    t = []
    s = []
    for i in range(10):
        obj = Actor([random.randrange(0, 500), random.randrange(0, 500)], "worker", 0.1 * random.random() + 1,
                    [[-5, -5], [5, -5], [5, 5], [-5, 5]], "worker" + str(i))
        w.append(obj)

    for i in range(5):
        obj = Actor([random.randrange(0, 500), random.randrange(0, 500)], "truck", 1.5 * random.random() + 1,
                    [[-10, -5], [-10, 5], [10, 5], [10, -5]], "truck" + str(i))
        t.append(obj)

    for i in range(5):
        obj = Structure([random.randrange(0, 500), random.randrange(0, 500)], "structure" + str(i))
        cond = True
        while cond:
            cond = False
            for e in s:
                if separating_axis_theorem(e.shape, obj.shape) or not separating_axis_theorem(obj.shape, _map.shape):
                    cond = True
                    obj = Structure([random.randrange(0, 500), random.randrange(0, 500)], "structure" + str(i))

        s.append(obj)



        # for i in range(150):
        #     obj = Activity([random.randrange(0, 500), random.randrange(0, 500)], "do work here", "active",
        #                   0, i)
        #     cond = True
        #     while cond:
        #         cond = False
        #         for e in s:
        #             if separating_axis_theorem(e.shape, obj.shape):
        #                 cond = True
        #                 obj = Activity([random.randrange(0, 500), random.randrange(0, 500)], "do work here", "active",
        #                               0, i)

        #  a.append(obj)

    data = {"actors": w + t, "structures": s}
    with open("sim.dat", "wb") as f:
        pickle.dump(data, f)


generateSim()
