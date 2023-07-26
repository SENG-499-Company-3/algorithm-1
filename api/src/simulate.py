import numpy as np
import matplotlib.pyplot as plt
import copy
from typing import Tuple
from hypergraph import HyperGraph


def probs(range_max: int, ndarr: np.ndarray) -> np.ndarray:
    lin_bins = np.arange(0, range_max)
    elem_counts, bins = np.histogram(ndarr, bins=lin_bins)
    probs = elem_counts / elem_counts.sum()
    return probs


def run_simulation(
    trials: int,
    shape: Tuple[int, int, int],
    pivots: np.ndarray,
    max_iter: int,
    p_tgt: int
    ) -> None:

    courses, times, teachers = shape
    dims = {"courses":courses, "times":times, "teachers":teachers}
    prefs = np.loadtxt('../data/formatted_prefs.csv', delimiter=',')
    loads = np.loadtxt('../data/formatted_loads.csv', delimiter=',')
    pref_ps = probs(8, prefs)
    load_ps = probs(6, loads) 
    P = np.arange(0, 7, dtype=np.uint8)
    L = np.arange(0, 5, dtype=np.uint8) 
    hypergraphs = np.ndarray(shape=trials, dtype=object)

    for i in range(trials):
        prefs = np.random.choice(P, size=(teachers, courses), p=pref_ps)
        loads = np.random.choice(L, size=teachers , p=load_ps)
        hg = HyperGraph(dims, prefs, loads, pivots, max_iter, P, p_tgt)
        hg.solve()
        hypergraphs[i] = hg
        
    np.save(f"../data/raw_experimental_results/uniform_inputs_{trials}_trials_{max_iter}_iters_{p_tgt}_ptgt", hypergraphs, allow_pickle=True)
