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
    valid: bool


class Schedule(BaseModel):
    iterations: Optional[int] = None
    quality: Optional[float] = None
    c_hat: Optional[float] = None
    reward: Optional[float] = None
    valid: Optional[bool] = None
    complete: Optional[bool] = None
    assignments: Optional[list] = None


class InputDataRooms(BaseModel):
    location: Optional[str] = None
    capacity: Optional[int] = None
    equipment: Optional[List[str]] = None


class InputDataTimeslots(BaseModel):
    day: Optional[List[str]] = None
    length: Optional[int] = None
    startTime: Optional[int] = None


class InputDataCourses(BaseModel):
    coursename: Optional[str] = None
    noScheduleOverlap: Optional[List[str]] = None
    lecturesNumber: Optional[int] = None
    labsNumber: Optional[int] = None
    tutorialsNumber: Optional[int] = None
    capacity: Optional[int] = None


class InputDataProfessors(BaseModel):
    name: Optional[str] = None
    courses: Optional[List[str]] = None
    timePreferences: Optional[List[str]] = None
    coursePreferences: Optional[List[str]] = None
    dayPreferences: Optional[List[str]] = None
    equipmentPreferences: Optional[List[str]] = None


class InputDataDimensions(BaseModel):
    courses: Optional[int] = None
    times: Optional[int] = None
    teachers: Optional[int] = None
    rooms: Optional[int] = None


class InputData(BaseModel):
    rooms: Optional[InputDataRooms] = None
    timeslots: Optional[InputDataTimeslots] = None
    courses: Optional[InputDataCourses] = None
    professors: Optional[InputDataProfessors] = None
    dimensions: Optional[List[InputDataDimensions]] = None
    preferences: Optional[List[List[int]]] = None
    loads: Optional[List[List[int]]] = None
    required_courses: Optional[List[int]] = None
    p_tgt: Optional[int] = None
    max_iter: Optional[int] = None
