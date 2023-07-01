import time
import multiprocessing as mp
import numpy as np
from typing import List, Union
from hypergraph import HyperGraph
from models import InputData



TIMEOUT = 60.0
courses, times, teachers = 33, 15, 29
dims = {"courses":courses, "times":times, "teachers":teachers}
prefs = np.loadtxt("../data/formatted_prefs.csv", delimiter=",")
#prefs = np.random.randint(7, size=(teachers, courses), dtype=np.uint64)
loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
pivots = [10,20,29,33]
max_iter = 1000
P = np.arange(0,7, dtype=np.uint64)
p_tgt = 4
num_workers = 1
batch_size = 5



def sequential_driver(input_data: InputData = None) -> Union[HyperGraph, None]:
    hg = HyperGraph(dims, prefs, loads, pivots, max_iter, P, p_tgt)
    start_time = time.time() 
    
    #while (start_time - time.time()) < TIMEOUT:
     
    hg.solve()
    return hg
        
    return None


def batch_driver(input_data: InputData = None) -> Union[HyperGraph, None]:
    hypergraphs = [HyperGraph(dims, prefs, loads, pivots, max_iter, P, p_tgt)] * batch_size
    start_time = time.time()
    
    while (start_time - time.time()) < TIMEOUT:
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
    return hypergraphs[0]
     
    return None


def distributed_driver(input_data: InputData = None) -> Union[HyperGraph, None]: 
    try:
        mp.set_start_method("spawn", force=True)
    
    except RuntimeError:
        pass

    with mp.get_context("spawn").Pool() as mp_pool:
        hg_type = type(HyperGraph(dims, prefs, loads, pivots, max_iter, P, p_tgt)) 
        ret_types = []
        start_time = time.time()
        
        while hg_type not in ret_types and (time.time() - start_time) < TIMEOUT:
            hg_pool = [
                [HyperGraph(dims, prefs, loads, pivots, max_iter, P, p_tgt)]
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


def distributed_batch_driver(input_data: InputData = None) -> Union[HyperGraph, None]:
    try:
        mp.set_start_method("spawn", force=True)
    
    except RuntimeError:
        pass

    with mp.get_context("spawn").Pool() as mp_pool:
        hg_type = type(HyperGraph(dims, prefs, loads, pivots, max_iter, P, p_tgt)) 
        ret_types = []
        start_time = time.time()
        
        while hg_type not in ret_types and (time.time() - start_time) < TIMEOUT:
            hg_pool = [
                [HyperGraph(dims, prefs, loads, pivots, max_iter, P, p_tgt)] * batch_size 
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
