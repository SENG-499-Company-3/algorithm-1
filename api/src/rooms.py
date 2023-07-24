from hypergraph import HyperGraph
from models import InputData, InputDataRooms
from hypergraph import *


def add_rooms(hypergraph: HyperGraph = None, input_data: InputData = None):
    time_blocks = [[] for _ in range(input_data.dimensions.times)]
    rooms_dict = {}

    courses = input_data.courses
    rooms = input_data.rooms

    for key in hypergraph.sparse_tensor:
        course_id, time, teacher = key
        time_blocks[int(time)].append((int(course_id), int(teacher), courses[int(course_id)].capacity))

    for time_block in range(len(time_blocks)):
        courses_in_block = time_blocks[time_block]
        courses_in_block.sort(reverse=True)
        assigned_classrooms = []

        for course in courses_in_block:
            assigned = False
            course_num = course[0]
            course_capacity = course[2]
            for classroom in rooms:
                class_capacity = classroom.capacity
                if 10 <= (class_capacity - course_capacity)*100/class_capacity <= 25 \
                        and classroom not in assigned_classrooms:
                    rooms_dict[course_num] = classroom
                    assigned_classrooms.append(classroom)
                    print("course {} with capacity {} in block {} -> classroom {} with capacity {}".format(course_num, course_capacity, time_block, classroom.location, classroom.capacity))
                    assigned = True
                    break
                if not assigned:
                    rooms_dict[course_num] = (InputDataRooms(location="", capacity=0, equipment=[]))
                    hypergraph.courses_without_rooms.append(course_num)
        assigned_classrooms.clear()
    return rooms_dict
