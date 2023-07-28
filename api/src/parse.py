import numpy as np
from models import InputData


def parse(input_data: InputData) -> None:
    if not input_data.p_tgt:
        input_data.p_tgt = 4

    if not input_data.max_iter:
        input_data.max_iter = 250
    
    input_data.dimensions.courses = len(input_data.courses)
    input_data.dimensions.times =   len(input_data.timeslots)
    input_data.loads =              [prof.load for prof in input_data.professors]  
    input_data.preferences =        []
     
    for prof in input_data.professors:
        if not prof.coursePreferences:
            input_data.preferences.append([0] * input_data.dimensions.courses)
            continue
        
        prof.coursePreferences.sort(key=lambda pref: pref.courseNumber)
        pref_course_dict = {pc.courseName:pc for pc in prof.coursePreferences}
        vals = []
        for course in input_data.courses:
            if course.coursename in pref_course_dict:
                vals.append(pref_course_dict[course.coursename].value)
            else:
                vals.append(0)

        input_data.preferences.append(vals)
    print(np.count_nonzero(input_data.preferences)) 
    input_data.dimensions.teachers = len(input_data.professors) 
    input_data.courses.sort(key=lambda course: course.courseNumber) 
    required_courses = {
        input_data.courses[i].courseYear : i+1 
        for i in range(input_data.dimensions.courses)
    }
    input_data.required_courses = list(required_courses.values())
