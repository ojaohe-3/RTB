import random
import unittest
import toml
import RTB.src.Emulator.actor
import RTB.src.Emulator.activity
import RTB.src.Emulator.structure
import time


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)



def main():
    w = []
    t = []
    a = []
    s = []
    for i in range(10):
        obj = RTB.Actor((random.randrange(0, 500), random.randrange(0, 500)), "worker", random.random, [(0, 0), (0, 1), (1, 1), (1, 0)], "worker" + i)
        w.append(obj)
    for i in range(5):
        obj = RTB.Actor((random.randrange(0, 500), random.randrange(0, 500)), "truck", 3*random.random,
                        [(0, 0), (0, 1), (2, 1), (2, 0)], "truck" + i)
        t.append(obj)
    for i in range(3):
        obj = RTB.Structure(None, (random.randrange(0, 500), random.randrange(0, 500)))
        s.append(obj)
    for i in range(10):
        obj = RTB.Activity((random.randrange(0, 500), random.randrange(0, 500),"do work here","active",time.time()+i*random.randrange(1,1000)))
        a.append(obj)
    msg = "[Activites]\n\t"
    for item in a:
        msg += "pos = ("+item.pos[0]+","+item.pos[1]+")\n\t"



if __name__ == '__main__':
    # unittest.main()
    main()