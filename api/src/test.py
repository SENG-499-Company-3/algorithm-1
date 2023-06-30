import numpy as np
from hypergraph import HyperGraph
import sys

np.set_printoptions(threshold=sys.maxsize)

courses, times, teachers = 20, 15, 30
dims = {"courses":courses, "times":times, "teachers":teachers}
prefs = np.random.randint(0,7,(teachers,courses))
loads = np.asarray([3] * 30)
pivots = [5,10,15,20]

hg = HyperGraph(dims, prefs, loads, pivots)
hg.solve()

print(f"prefs: {prefs}\n\npreferred_tc: {hg.get_preferred(0,5)}\n\nhg: {hg.sparse()}")

