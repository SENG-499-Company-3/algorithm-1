import numpy as np
from hypergraph import HyperGraph
from search_drivers import distributed_driver
import sys

np.set_printoptions(threshold=sys.maxsize)

courses, times, teachers = 33, 15, 29
dims = {"courses":courses, "times":times, "teachers":teachers}
#prefs = np.loadtxt("formatted_prefs.csv", delimiter=",")
prefs = np.random.randint(7, size=(teachers, courses), dtype=np.uint64)
loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
pivots = [5,10,15,20,25,33]
max_iter = 5000
P = np.arange(0,7, dtype=np.uint64)
p_tgt = 4

hg = HyperGraph(dims, prefs, loads, pivots, max_iter, P, p_tgt)
hg.solve()
print(f"valid: {hg.is_valid_schedule()}\nreward: {hg.calc_reward()}\nassignments: {hg.sparse()}")


