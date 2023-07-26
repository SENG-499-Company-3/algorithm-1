from __future__ import annotations
from models import InputData, Assignment, Schedule, IsValidSchedule
from drivers import distributed_driver
from hypergraph import HyperGraph
from rooms import add_rooms, validate_rooms


def is_schedule_valid(schedule: Schedule):
    is_valid = validate_rooms(schedule)
    # schedule.is_valid_schedule()
    return IsValidSchedule(valid=is_valid)


def generate_schedule(input_data: InputData):
    hypergraph = distributed_driver(input_data)
    rooms_dict = add_rooms(hypergraph, input_data)
    assignments_list = []

    for key in hypergraph.sparse_tensor:
        course, time, teacher = key
        assignment = Assignment(
            course=input_data.courses[course],
            prof=input_data.professors[teacher],
            timeslot=input_data.timeslots[time],
            room=rooms_dict[course]
        )
        Assignment.update_forward_refs()
        assignments_list.append(assignment)

    schedule = Schedule(
        iterations=hypergraph.iter,
        quality=hypergraph.quality,
        c_hat=hypergraph.c_hat,
        reward=hypergraph.reward,
        valid=hypergraph.is_valid_schedule(),
        complete=hypergraph.is_complete(),
        assignments=assignments_list
    )

    return schedule
