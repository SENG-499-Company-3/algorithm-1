import numpy as np
from models import InputData


def parse(input_data: InputData) -> None:
    if not input_data.p_tgt:
        input_data.p_tgt = 4

    if not input_data.max_iter:
        input_data.max_iter = 250
    
    input_data.dimensions.courses =  len(input_data.courses)
    input_data.dimensions.times =    len(input_data.timeslots)
    input_data.dimensions.teachers = len(input_data.professors) 
    input_data.loads =               [prof.load for prof in input_data.professors]  
    input_data.preferences =         []

    for prof in input_data.professors:
        prof.coursePreferences.sort(key=lambda pref: pref.courseNumber)
        input_data.preferences.append([prof.coursePreferences.value])
    
    input_data.courses.sort(key=lambda course: course.courseNumber) 
    required_courses = {
        input_data.courses[i].courseYear : i+1 
        for i in range(input_data.dimensions.courses)
    }
    input_data.required_courses = list(required_courses.values())
