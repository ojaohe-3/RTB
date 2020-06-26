import random
import unittest
import toml
from src.Emulator.activity import Activity
from src.Emulator.actor import Actor
from src.Emulator.structure import Structure
import time
import pickle


def generateSim():
    w = []
    t = []
    a = []
    s = []
    for i in range(10):
        obj = Actor([random.randrange(0, 500), random.randrange(0, 500)], "worker", random.random(),
                    [[-1, -1], [1, -1], [1, 1], [-1, 1]], "worker" + str(i))
        w.append(obj)
    for i in range(5):
        obj = Actor([random.randrange(0, 500), random.randrange(0, 500)], "truck",  3*random.random(),
                    [[-2, -1], [-2, 1], [2, 1], [2, -1]], "truck" + str(i))
        t.append(obj)
    for i in range(3):
        obj = Structure([random.randrange(0, 500), random.randrange(0, 500)])
        s.append(obj)
    for i in range(150):
        obj = Activity([random.randrange(0, 500), random.randrange(0, 500)], "do work here", "active",
                       time.time() + i * random.randrange(1, 1000))
        a.append(obj)

    data = {"activites": a, "actors": w + t, "structures": s}
    with open("sim.dat", "wb") as f:
        pickle.dump(data, f)


generateSim()
