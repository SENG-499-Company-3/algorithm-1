import multiprocessing as mp
import numpy as np
from typing import List, Union
from hypergraph import HyperGraph
from models import InputData



courses, times, teachers = 33, 15, 29
dims = {"courses":courses, "times":times, "teachers":teachers}
prefs = np.random.randint(7, size=(teachers, courses), dtype=np.uint64)
loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
pivots = np.array([10,20,27,33], dtype=np.uint64)
max_iter = 500
P = np.arange(0,7, dtype=np.uint64)
p_tgt = 4
num_workers = 8
batch_size = 1



def sequential_driver(input_data: InputData = None) -> HyperGraph:
    hg = HyperGraph(dims, prefs, loads, pivots, max_iter, P, p_tgt)
    hg.solve()
    return hg


def async_solve(hg: HyperGraph) -> Union[HyperGraph, None]:
    hg.solve()
    return hg 


def distributed_driver(input_data: InputData = None) -> Union[HyperGraph, None]: 
    try:
        mp.set_start_method("spawn", force=True)
    
    except RuntimeError:
        pass

    with mp.get_context("spawn").Pool(num_workers) as mp_pool:
        hg = HyperGraph(dims, prefs, loads, pivots, max_iter, P, p_tgt)
        hg_type = type(hg) 
        hypergraphs = [hg] * batch_size
        res = mp_pool.map(async_solve, hypergraphs)
    
    valid_schedules = [schd for schd in res if isinstance(schd, hg_type)] 
    
    if not valid_schedules: 
        return None
    
    valid_schedules.sort(key = lambda hg: hg.reward)
    return valid_schedules[0]
