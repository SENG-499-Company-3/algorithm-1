from models import *
from drivers import distributed_driver
from hypergraph import HyperGraph
from rooms import add_rooms

default_input_data = InputData(rooms=[InputDataRooms(location="ECS 123", capacity=130, equipment=[]),
                                      InputDataRooms(location="ECS 120", capacity=210, equipment=[]),
                                      InputDataRooms(location="ECS 111", capacity=20, equipment=[]),
                                      InputDataRooms(location="ECS 100", capacity=210, equipment=[])],
                               timeslots=[InputDataTimeslots(day=["Monday", "Thursday"], length=80, startTime=830),
                                          InputDataTimeslots(day=["Monday", "Thursday"], length=80, startTime=1000),
                                          InputDataTimeslots(day=["Monday", "Thursday"], length=80, startTime=1130),
                                          InputDataTimeslots(day=["Monday", "Thursday"], length=80, startTime=1300),
                                          InputDataTimeslots(day=["Monday", "Thursday"], length=80, startTime=1430),
                                          InputDataTimeslots(day=["Monday", "Thursday"], length=80, startTime=1600),
                                          InputDataTimeslots(day=["Tuesday", "Wednesday", "Friday"], length=50, startTime=830),
                                          InputDataTimeslots(day=["Tuesday", "Wednesday", "Friday"], length=50, startTime=930),
                                          InputDataTimeslots(day=["Tuesday", "Wednesday", "Friday"], length=50, startTime=1030),
                                          InputDataTimeslots(day=["Tuesday", "Wednesday", "Friday"], length=50, startTime=1130),
                                          InputDataTimeslots(day=["Tuesday", "Wednesday", "Friday"], length=50, startTime=1230),
                                          InputDataTimeslots(day=["Tuesday", "Wednesday", "Friday"], length=50, startTime=1330),
                                          InputDataTimeslots(day=["Tuesday", "Wednesday", "Friday"], length=50, startTime=1430),
                                          InputDataTimeslots(day=["Tuesday", "Wednesday", "Friday"], length=50, startTime=1530),
                                          InputDataTimeslots(day=["Tuesday", "Wednesday", "Friday"], length=50, startTime=1630)
                                          ],
                               courses=[InputDataCourses(coursename="CSC 130", capacity=100),
                                        InputDataCourses(coursename="CSC 111", capacity=170),
                                        InputDataCourses(coursename="CSC 123", capacity=15),
                                        InputDataCourses(coursename="CSC 144", capacity=172)],
                               professors=[
                                   InputDataProfessors(name="Dr. Smith",
                                                       courses=["CSC 130", "CSC 111", "CSC 123", "CSC 144"],
                                                       timePreferences=[], coursePreferences=[], dayPreferences=[],
                                                       equipmentPreferences=[]),
                                   InputDataProfessors(name="Dr. Jones",
                                                       courses=["CSC 130", "CSC 111", "CSC 123", "CSC 144"],
                                                       timePreferences=[], coursePreferences=[], dayPreferences=[],
                                                       equipmentPreferences=[]),
                                   InputDataProfessors(name="Dr. Brown",
                                                       courses=["CSC 130", "CSC 111", "CSC 123", "CSC 144"],
                                                       timePreferences=[], coursePreferences=[], dayPreferences=[],
                                                       equipmentPreferences=[]),
                                   InputDataProfessors(name="Dr. White",
                                                       courses=["CSC 130", "CSC 111", "CSC 123", "CSC 144"],
                                                       timePreferences=[], coursePreferences=[], dayPreferences=[],
                                                       equipmentPreferences=[]),
                               ],
                               dimensions=InputDataDimensions(courses=4, times=15, teachers=4, rooms=4),
                               preferences=[[6, 0, 0, 0], [0, 6, 0, 0], [0, 0, 6, 0], [0, 0, 0, 6]],
                               loads=[3, 3, 3, 3],
                               required_courses=[4],
                               max_iter=500,
                               p_tgt=4)


def generate_schedule(input_data: InputData = None):
    if input_data is None:
        input_data = default_input_data

    hypergraph = distributed_driver(input_data)
    rooms_dict = add_rooms(hypergraph, input_data)
    assignments_list = []

    Assignment.update_forward_refs()
    for key in hypergraph.sparse_tensor:
        course, time, teacher = key
        assignments_list.append(
            Assignment(course=input_data.courses[course], prof=input_data.professors[teacher],
                       timeslot=input_data.timeslots[time], room=rooms_dict[course]))

    if len(assignments_list) != len(hypergraph.sparse_tensor):
        raise Exception("Assignments list is not the same length as the sparse tensor")

    schedule = Schedule(iterations=hypergraph.iter, quality=hypergraph.quality, c_hat=hypergraph.c_hat,
                        reward=hypergraph.reward, valid=hypergraph.is_valid_schedule(),
                        complete=hypergraph.is_complete(), assignments=assignments_list)
    print_schedule(schedule)
    return schedule


def print_schedule(schedule: Schedule):
    for assignment in schedule.assignments:
        print(
            f"{assignment.course.coursename} predicted capacity:{assignment.course.capacity} \n{assignment.prof.name}\n{assignment.timeslot.day} {assignment.timeslot.startTime}\n{assignment.room.location} room capacity {assignment.room.capacity}\n")
