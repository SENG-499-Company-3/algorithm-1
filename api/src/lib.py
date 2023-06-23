import time
import multiprocessing as mp
import numpy as np
from typing import Union
from hypergraph import HyperGraph
from models import InputData

def preprocess(fname: str = "prefs.csv") -> np.ndarray:
    val_map = {0: 0, 20: 1, 39: 2, 40: 3, 78: 4, 100: 5, 195: 6}
    prefs = np.loadtxt(fname, delimiter=",", dtype=np.uint64)
    rows, cols = prefs.shape
    for i in range(rows):
        for j in range(cols):
            prefs[i, j] = val_map[prefs[i, j]]
    return prefs

def random_search(req_body: InputData = None) -> Union[HyperGraph, None]:
    courses = 33
    times = 51
    teachers = 29

    dims = {"courses": courses, "times": times, "teachers": teachers}

    prefs = np.random.randint(7, size=(teachers, courses), dtype=np.uint64)
    loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
    max_iter = 2500
    P = np.array([0, 1, 2, 3, 4, 5, 6], dtype=np.uint64)
    p_tgt = 3

    timeout = 60

    start_time = time.time()
    while (start_time - time.time()) < timeout:
        hg = HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)
        hg.solve()
        if hg.is_valid_schedule():
            return hg
    return None


def batch_search(req_body: InputData = None) -> Union[HyperGraph, None]:
    courses = 33
    times = 51
    teachers = 29

    dims = {"courses": req_body.dimensions.courses, "times": req_body.dimensions.times, "teachers": req_body.dimensions.teachers}

    prefs = np.random.randint(7, size=(teachers, courses), dtype=np.uint64)
    loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
    max_iter = 2500
    P = np.array([0, 1, 2, 3, 4, 5, 6], dtype=np.uint64)
    p_tgt = InputData.p_tgt

    timeout = 60
    batch_size = 5 

    start_time = time.time()
    while (start_time - time.time()) < timeout:
        hypergraphs = [HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)] * batch_size

        for hg in hypergraphs:
            hg.solve()
        
        hypergraphs.sort(key = lambda hg: hg.calc_reward())

        for hg in hypergraphs:
            if hg.is_valid_schedule() == True:
                return hg
        
    return None
   

def async_solve(hg: HyperGraph) -> Union[HyperGraph, None]:
    hg.solve()
    if hg.is_valid_schedule():
        return hg
    return None


def distributed_search(req_body: InputData = None) -> Union[HyperGraph, None]:
    courses = 33
    times = 51
    teachers = 29

    dims = {"courses": courses, "times": times, "teachers": teachers}

    prefs = np.random.randint(7, size=(teachers, courses), dtype=np.uint64)
    #prefs = np.loadtxt("formatted_prefs.csv", delimiter=",")
    loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
    max_iter = 2500
    P = np.array([0, 1, 2, 3, 4, 5, 6], dtype=np.uint64)
    p_tgt = 3
    num_workers = 8
    
    try:
        mp.set_start_method("spawn", force=True)
    
    except RuntimeError:
        pass

    with mp.get_context("spawn").Pool() as mp_pool:
        hg_type = type(HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)) 
        ret_types = []
        max_runtime = 60
        start_time = time.time()
        while hg_type not in ret_types and (time.time() - start_time) < max_runtime:
            hg_pool = [
                HyperGraph(dims, prefs, loads, max_iter, P, p_tgt) 
                for i in range(num_workers)
            ]
            res = mp_pool.map(async_solve, req_body)
            ret_types = [type(graph) for graph in res]
    
    valid_schedules = [
        schd for schd in res if isinstance(schd, hg_type)
    ] 
    
    if len(valid_schedules) > 0:
        valid_schedules.sort(key = lambda hg: hg.calc_reward())
        return valid_schedules[0]
    
    return None
