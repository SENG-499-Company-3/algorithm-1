import multiprocessing as mp
import numpy as np
from typing import List, Union
from hypergraph import HyperGraph
from models import InputData

courses, times, teachers, num_rooms = 33, 15, 29, 123
dims = {"courses": courses, "times": times, "teachers": teachers, "rooms": num_rooms}
prefs = np.random.randint(7, size=(teachers, courses), dtype=np.uint64)
loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
pivots = np.array([10,20,27,33], dtype=np.uint64)
max_iter = 500
P = np.arange(0, 7, dtype=np.uint64)
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
    dims = {
        "courses":  input_data.dimensions.courses, 
        "times":    input_data.dimensions.times, 
        "teachers": input_data.dimensions.teachers
    }
    prefs = np.asarray(input_data.preferences)
    loads = np.asarray(input_data.loads)
    pivots = np.asarray(input_data.required_courses)
    max_iter = input_data.max_iter 
    p_tgt = input_data.p_tgt
    
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
    valid_schedules[0].add_rooms()
    return valid_schedules[0]
