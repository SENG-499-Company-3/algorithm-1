import multiprocessing as mp
import numpy as np
from typing import List, Union
from hypergraph import HyperGraph
from models import InputData, Schedule, IsValidSchedule
from simulate import probs


courses, times, teachers, num_rooms = 33, 15, 29, 123
dims = {"courses": courses, "times": times, "teachers": teachers, "rooms": num_rooms}
prefs_og = np.loadtxt('./formatted_prefs.csv', delimiter=',')
loads_og = np.loadtxt('./formatted_loads.csv', delimiter=',')
P = np.arange(0,7, dtype=np.uint64)
L = np.arange(0, 5, dtype=np.uint64)
prefs = np.random.choice(P, size=(teachers, courses), p=probs(8, prefs_og))
loads = np.random.choice(L, size=teachers, p=probs(6, loads_og))
pivots = np.array([6,13,24,33], dtype=np.uint64)
max_iter = 500
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
    courses =  len(input_data.courses)
    teachers = len(input_data.professors)
    times =    len(input_data.timeslots)
    dims = {
        "courses":  courses,
        "times":    times,
        "teachers": teachers
    }
    pivots = np.asarray(input_data.required_courses)
    max_iter = input_data.max_iter
    p_tgt = input_data.p_tgt
    loads = np.asarray([prof.load for prof in input_data.professors])
    prefs = np.zeros(shape=(teachers, courses), dtype=np.uint8) 
    parsed_preferences = [np.asarray(prof.coursePreferences) for prof in input_data.professors]  
    
    for i in range(len(parsed_preferences)):
        row = parsed_preferences[i]
        prefs[i, :] = row[:]

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

    valid_schedules.sort(key=lambda hg: hg.reward)
    return valid_schedules[0]


def validate_driver(schedule: Schedule = None) -> IsValidSchedule:
    input_data = schedule.inputData
    dims = {
        "courses" :  input_data.dimensions.courses,
        "times" :    input_data.dimensions.times,
        "teachers" : input_data.dimensions.teachers
    }
    pivots = np.asarray(input_data.required_courses)
    prefs = np.asarray(input_data.preferences)
    loads = np.asarray(input_data.loads)
    max_iter = input_data.max_iter
    p_tgt = input_data.p_tgt
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
        booked_room = (ass.room.location, ass.timeslot.startTime, ass.timeslot.day[0])
        if booked_room in rooms:
            return IsValidSchedule(valid=False)
        rooms.add(booked_room)
        sparse_tensor[(ass.course.index, ass.timeslot.index, ass.prof.index)] = 1
     
    return IsValidSchedule(valid=hg.is_valid_schedule(sparse_tensor))
