from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


class Error(BaseModel):
    message: str = Field(..., description='Error message')
    errors: Error


class Success(BaseModel):
    success: bool = Field(..., description='Success')
    message: str = Field(..., description='Success message')


class IsValidSchedule(BaseModel):
    valid: Optional[bool] = None


class InputDataRooms(BaseModel):
    location: Optional[str] = None
    capacity: Optional[int] = None


class InputDataTimeslots(BaseModel):
    day: Optional[List[str]] = None
    length: Optional[int] = None
    startTime: Optional[int] = None
    index: Optional[int] = None


class InputDataCourses(BaseModel):
    coursename: Optional[str] = None
    courseYear: Optional[int] = None
    courseNumber: Optional[int] = None
    capacity: Optional[int] = None
    index: Optional[int] = None


class InputDataProfessorsCoursePreferences(BaseModel):
    email: Optional[str] = None
    load: Optional[int] = None
    courseName: Optional[str] = None
    courseNumber: Optional[int] = None
    courseYear: Optional[int] = None
    value: Optional[int] = None
        

class InputDataProfessors(BaseModel):
    name: Optional[str] = None
    coursePreferences: Optional[List[InputDataProfessorsCoursePreferences]] = None
    load: Optional[int] = None
    index: Optional[int] = None


class InputDataDimensions(BaseModel):
    courses: Optional[int] = None
    times: Optional[int] = None
    teachers: Optional[int] = None
    rooms: Optional[int] = None


class Assignment(BaseModel):
    course: InputDataCourses
    prof: InputDataProfessors
    timeslot: InputDataTimeslots
    room: InputDataRooms


class InputData(BaseModel):
    rooms: Optional[List[InputDataRooms]] = None
    timeslots: Optional[List[InputDataTimeslots]] = None
    courses: Optional[List[InputDataCourses]] = None
    professors: Optional[List[InputDataProfessors]] = None
    dimensions: Optional[InputDataDimensions] = None
    preferences: Optional[List[List[int]]] = None
    loads: Optional[List[int]] = None
    required_courses: Optional[List[int]] = None
    p_tgt: Optional[int] = None
    max_iter: Optional[int] = None


class Schedule(BaseModel):
    iterations: int
    quality: float
    valid: bool
    complete: bool
    reward: float
    c_hat: float
    assignments: List[Assignment]
    inputData: Optional[InputData] = None
