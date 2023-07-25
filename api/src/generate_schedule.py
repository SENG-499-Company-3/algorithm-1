from __future__ import annotations
import itertools
from typing import Optional
from models import InputData, Assignment, Schedule
from drivers import distributed_driver
from hypergraph import HyperGraph
from rooms import add_rooms


def generate_schedule(input_data: InputData):
    hg = distributed_driver(input_data)
    rooms_dict = add_rooms(hg, input_data)
    assignments_list = []

    for assignment_tuple in hg.sparse_tensor:
        course, time, teacher = assignment_tuple
        c_obj = input_data.courses[course]
        p_obj = input_data.professors[teacher]
        t_obj = input_data.timeslots[time] 
        r_obj = rooms_dict[course] 
        c_obj.index = course
        p_obj.index = teacher
        t_obj.index = time
        assignment = Assignment( 
            course = c_obj,
            prof = p_obj,
            timeslot = t_obj, 
            room = r_obj
        )
        assignment.prof.load -= 1
        assignments_list.append(assignment)
    
    input_data.preferences =      [list(pref_row) for pref_row in hg.prefs]
    input_data.loads =            list(hg.loads)
    input_data.required_courses = list(hg.pivots)
    schedule = Schedule(
        iterations =    int(hg.iter), 
        quality =       float(hg.quality), 
        c_hat =         float(hg.c_hat),
        reward =        float(hg.reward), 
        valid =         bool(hg.is_valid_schedule()),
        complete =      bool(hg.is_complete()), 
        assignments =   assignments_list,
        inputData =     input_data,
        sparse_tensor = list(hg.sparse_tensor.keys())
    )
    
    return schedule
