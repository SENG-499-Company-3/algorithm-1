import time
import multiprocessing as mp
import numpy as np
from typing import Union, List
from hypergraph import HyperGraph
from models import InputData


TIMEOUT = 60
courses = 33
times = 51
teachers = 29
dims = {"courses": courses, "times": times, "teachers": teachers}
#prefs = np.loadtxt("formatted_prefs.csv", delimiter=",")
prefs = np.random.randint(7, size=(teachers, courses), dtype=np.uint64)
loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
max_iter = 1500
P = np.array([0, 1, 2, 3, 4, 5, 6], dtype=np.uint64)
p_tgt = 4



def preprocess(fname: str = "prefs.csv") -> np.ndarray:
    val_map = {0: 0, 20: 1, 39: 2, 40: 3, 78: 4, 100: 5, 195: 6}
    prefs = np.loadtxt(fname, delimiter=",", dtype=np.uint64)
    rows, cols = prefs.shape
    
    for i in range(rows):
        for j in range(cols):
            prefs[i, j] = val_map[prefs[i, j]]
    
    return prefs


def numpy_to_fastapi_type_conversion(hg: HyperGraph) -> List[List[int]]:
    items = hg.sparse().items()

    fastapi_type_compatible_assignments = [
        [num.item() for num in key]
        for key, _ in items
    ]
    
    return fastapi_type_compatible_assignments 


def sequential_search(input_data: InputData = None) -> Union[HyperGraph, None]:
    hg = HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)
    start_time = time.time() 
    
    while (start_time - time.time()) < TIMEOUT:
        hg.solve()
        if hg.is_valid_schedule():
            return hg

    return None


def batch_search(input_data: InputData = None) -> Union[HyperGraph, None]:
    batch_size = 5 
    start_time = time.time()
    
    while (start_time - time.time()) < TIMEOUT:
        hypergraphs = [HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)] * batch_size

        for hg in hypergraphs:
            hg.solve()
        
        hypergraphs.sort(key = lambda hg: hg.calc_reward())

        for hg in hypergraphs:
            if hg.is_valid_schedule() == True:
                return hg
        
    return None
   

def async_solve(hypergraphs: List[HyperGraph]) -> Union[HyperGraph, None]:
    for hg in hypergraphs:
        hg.solve()
    
    hypergraphs.sort(key = lambda hg: hg.calc_reward())
    
    for hg in hypergraphs:
        if hg.is_valid_schedule():
            return hg
        
    return None


def distributed_sequential_search(input_data: InputData = None) -> Union[HyperGraph, None]:
    num_workers = 4
    batch_size = 5
    
    try:
        mp.set_start_method("spawn", force=True)
    
    except RuntimeError:
        pass

    with mp.get_context("spawn").Pool() as mp_pool:
        hg_type = type(HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)) 
        ret_types = []
        start_time = time.time()
        
        while hg_type not in ret_types and (time.time() - start_time) < TIMEOUT:
            hg_pool = [
                [HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)]
                for i in range(num_workers)
            ]
            res = mp_pool.map(async_solve, hg_pool)
            ret_types = [type(graph) for graph in res]
    
    valid_schedules = [
        schd for schd in res if isinstance(schd, hg_type)
    ] 
    
    if len(valid_schedules) > 0:
        valid_schedules.sort(key = lambda hg: hg.calc_reward())
        return valid_schedules[0]
    
    return None


def distributed_batch_search(input_data: InputData = None) -> Union[HyperGraph, None]:
    num_workers = 4
    batch_size = 5
    
    try:
        mp.set_start_method("spawn", force=True)
    
    except RuntimeError:
        pass

    with mp.get_context("spawn").Pool() as mp_pool:
        hg_type = type(HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)) 
        ret_types = []
        start_time = time.time()
        
        while hg_type not in ret_types and (time.time() - start_time) < TIMEOUT:
            hg_pool = [
                [HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)] * batch_size 
                for i in range(num_workers)
            ]
            res = mp_pool.map(async_solve, hg_pool)
            ret_types = [type(graph) for graph in res]
    
    valid_schedules = [
        schd for schd in res if isinstance(schd, hg_type)
    ] 
    
    if len(valid_schedules) > 0:
        valid_schedules.sort(key = lambda hg: hg.calc_reward())
        return valid_schedules[0]
    
    return None
