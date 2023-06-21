import numpy as np


val_map = {0 : 0, 20 : 1, 39 : 2, 40 : 3, 78 : 4, 100 : 5, 195 : 6}


def preprocess(fname="prefs.csv"):
    prefs = np.loadtxt(fname, delimiter=",", dtype=np.uint64)
    rows, cols = prefs.shape
    for i in range(rows):
        for j in range(cols):
            prefs[i, j] = val_map[prefs[i, j]]
    return prefs
