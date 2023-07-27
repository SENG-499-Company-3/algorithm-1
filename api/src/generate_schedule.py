from __future__ import annotations
from models import InputData, Assignment, Schedule
from drivers import sequential_driver, distributed_driver
from hypergraph import HyperGraph
from rooms import add_rooms


def generate_schedule(input_data: InputData) -> Schedule:
    hg = sequential_driver(input_data)
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
        p_obj.load -= 1
        assignment = Assignment( 
            course = c_obj,
            prof = p_obj,
            timeslot = t_obj, 
            room = r_obj
        )
        assignments_list.append(assignment)
    
    schedule = Schedule(
        iterations =    int(hg.iter), 
        quality =       float(hg.quality), 
        c_hat =         float(hg.c_hat),
        reward =        float(hg.reward), 
        valid =         bool(hg.is_valid_schedule()),
        complete =      bool(hg.is_complete()), 
        assignments =   assignments_list,
        inputData =     input_data,
    )
    
    return schedule
