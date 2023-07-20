import numpy as np
import matplotlib.pyplot as plt
import copy
from typing import Tuple
from hypergraph import HyperGraph



def pref_probs(prefs: np.ndarray) -> np.ndarray:
    p_counts, bins = np.histogram(prefs, bins=np.arange(0,8))
    pref_probs = p_counts/p_counts.sum()
    return pref_probs


def load_probs(loads: np.ndarray) -> np.ndarray:
    p_counts, bins = np.histogram(loads, bins=np.arange(0,8))
    load_probs = p_counts/p_counts.sum()
    return load_probs


def run_simulation(trials: int) -> None:
    courses, times, teachers = 33, 15, 29
    dims = {"courses":courses, "times":times, "teachers":teachers}
    prefs = np.loadtxt('../../data/formatted_prefs.csv', delimiter=',')
    loads = np.loadtxt('../../data/formatted_loads.csv', delimiter=',')
    pref_ps = pref_probs(prefs)
    load_ps = load_probs(loads)
    pivots = np.array([6,13,24,33], dtype=np.uint64)
    max_iter = 500
    P = np.arange(0, 7, dtype=np.uint64)
    L = np.arange(0, 7, dtype=np.uint64)
    p_tgt = 4
    hypergraphs = np.ndarray(shape=trials, dtype=object)
    
    for i in range(trials):
        prefs = np.random.choice(P, size=(teachers, courses), p=pref_ps)
        loads = np.random.choice(L, size=(teachers,) , p=load_ps)
        hg = HyperGraph(dims, prefs, loads, pivots, max_iter, P, p_tgt)
        hg.solve()
        hypergraphs[i] = hg
        
    np.save(f"../../data/simulated_hypergraphs_trials_{trials}", hypergraphs)
