from hypergraph import HyperGraph
from models import InputData, InputDataRooms
from hypergraph import *


def add_rooms(hypergraph: HyperGraph = None):
    time_blocks = [[] for _ in range(15)]
    rooms_list = []

    for key in hypergraph.sparse_tensor:
        course_id, time, teacher = key
        # access course capacity from input data when available
        random_capacity = random.randint(1, 250)
        time_blocks[int(time)].append((int(course_id), int(teacher), random_capacity))

    for time_block in range(len(time_blocks)):
        courses_in_block = time_blocks[time_block]
        courses_in_block.sort(reverse=True)
        assigned_classrooms = set()

        for course in courses_in_block:
            assigned = False
            course_num = course[0]
            course_prof = course[1]
            course_capacity = course[2]
            for (classroom, class_capacity) in ROOMS:
                if class_capacity >= course_capacity and (class_capacity - course_capacity) >= 25 and ROOMS.index((classroom, class_capacity)) not in assigned_classrooms:
                    rooms_list.append(InputDataRooms(location=classroom, capacity=class_capacity, equipment=[]))
                    assigned_classrooms.add(ROOMS.index((classroom, class_capacity)))
                    #print("course {} with capacity {} in block {} -> classroom {} with capacity {}".format(course_num, course_capacity, time_block, classroom, class_capacity))
                    assigned = True
                    break
            if not assigned:
                rooms_list.append(InputDataRooms(location="", capacity=0, equipment=[]))
                hypergraph.courses_without_rooms.append(course_num)
        assigned_classrooms.clear()
    return rooms_list
