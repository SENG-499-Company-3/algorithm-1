import multiprocessing as mp
import numpy as np
from typing import List, Union
from hypergraph import HyperGraph
from models import InputData, Schedule, IsValidSchedule
from simulate import probs


P = np.arange(0, 7, dtype=np.uint8)


def sequential_driver(input_data: InputData = None) -> HyperGraph:
    dims = {
        "courses"  : input_data.dimensions.courses,
        "times"    : input_data.dimensions.times,
        "teachers" : input_data.dimensions.teachers
    }
    pivots =   np.asarray(input_data.required_courses, dtype=np.uint64)
    loads =    np.asarray(input_data.loads, np.uint64)
    prefs =    np.asarray([np.asarray(row) for row in input_data.preferences], np.uint8)
    max_iter = input_data.max_iter
    p_tgt =    input_data.p_tgt  
    hg =       HyperGraph(dims, prefs, loads, pivots, max_iter, P, p_tgt)
    hg.solve()
    return hg


def async_solve(hg: HyperGraph) -> Union[HyperGraph, None]:
    hg.solve()
    return hg


def distributed_driver(input_data: InputData = None) -> Union[HyperGraph, None]:
    num_workers = 4
    batch_size = 1
    dims = {
        "courses"  : input_data.dimensions.courses,
        "times"    : input_data.dimensions.times,
        "teachers" : input_data.dimensions.teachers
    }
    prefs =    np.asarray([np.asarray(row) for row in input_data.preferences], np.uint8)
    loads =    np.asarray(input_data.loads, np.uint64)
    pivots =   np.asarray(input_data.required_courses, dtype=np.uint64)
    max_iter = input_data.max_iter
    p_tgt =    input_data.p_tgt 
    
    try:
        mp.set_start_method("spawn", force=True)

    except RuntimeError:
        pass

    with mp.get_context("spawn").Pool(num_workers) as mp_pool:
        hg =          HyperGraph(dims, prefs, loads, pivots, max_iter, P, p_tgt)
        hg_type =     type(hg)
        hypergraphs = [hg] * batch_size
        res =         mp_pool.map(async_solve, hypergraphs)

    valid_schedules = [schd for schd in res if isinstance(schd, hg_type)]

    if not valid_schedules:
        return None

    valid_schedules.sort(key=lambda hg: hg.reward)
    return valid_schedules[0]


def validate_driver(schedule: Schedule = None) -> IsValidSchedule:
    input_data = schedule.inputData
    dims = {
        "courses"  : input_data.dimensions.courses,
        "times"    : input_data.dimensions.times,
        "teachers" : input_data.dimensions.teachers
    }
    prefs =      np.asarray([np.asarray(row) for row in input_data.preferences], np.uint8)
    loads =      np.asarray(input_data.loads, dtype=np.uint64)
    pivots =     np.asarray(input_data.required_courses, np.uint64)
    max_iter =   input_data.max_iter
    p_tgt =      input_data.p_tgt
    hg = HyperGraph(
        dims, 
        prefs, 
        loads, 
        pivots, 
        max_iter, 
        P, 
        p_tgt
    )
    assignments = schedule.assignments
    sparse_tensor = {}
    rooms = set()
    
    for ass in assignments:
        if ass.timeslot.day:
            booked_room = (ass.room.location, ass.timeslot.startTime, ass.timeslot.day[0])

        else:
            continue

        if booked_room in rooms:
            return IsValidSchedule(valid=False)
        
        rooms.add(booked_room)
        sparse_tensor[(ass.course.index, ass.timeslot.index, ass.prof.index)] = 1
     
    return IsValidSchedule(valid=hg.is_valid_schedule(sparse_tensor))
