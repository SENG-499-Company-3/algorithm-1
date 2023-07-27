import numpy as np
from models import InputData


def parse(input_data: InputData) -> None:
    if not input_data.p_tgt:
        input_data.p_tgt = 4

    if not input_data.max_iter:
        input_data.max_iter = 500
    
    input_data.dimensions.courses =  len(input_data.courses)
    input_data.dimensions.times =    len(input_data.timeslots)
    input_data.dimensions.teachers = len(input_data.professors) 
    input_data.preferences =         [prof.coursePreferences for prof in input_data.professors]   
    input_data.loads =               [prof.load for prof in input_data.professors] 
    input_data.courses.sort(key=lambda course: course.coursename.split()[1]) 
    required_courses = {
        int(input_data.courses[i].coursename.split()[1][0]) : i+1 
        for i in range(input_data.dimensions.courses)
    }
    input_data.required_courses = list(required_courses.values())
