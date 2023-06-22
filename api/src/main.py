from __future__ import annotations

from typing import Union
import numpy as np
from fastapi import FastAPI
from hypergraph import HyperGraph
from lib import preprocess
from models import Success, Error, InputData, IsValidSchedule, Schedule
from ray import serve


app = FastAPI(
    title="SENG 499 API",
    description="This is SENG 499 Company 3 API",
    contact={
        "name": "Kjartan Einarsson",
        "url": "https://github.com/orgs/SENG-499-Company-3/projects/1/views/1",
        "email": "kjartanreinarsson@gmail.com",
    },
    version="1.0.2",
    servers=[
        {
            "url": "https://virtserver.swaggerhub.com/seng_499_api/BackendApi/1.0.0",
            "description": "SwaggerHub API Auto Mocking",
        },
        {"url": "http://localhost:3001", "description": "Local server"},
    ],
)

'''
@app.post(
    "/schedule/create",
    response_model=Schedule,
    responses={"400": {"model": Error}},
    tags=["algorithm1"],
)
def create_schedule(body: InputData = None) -> Union[Schedule, Error]:
    """
    Algorithm 1 endpoint to generate a schedule
    """
    courses = 33
    times = 51
    teachers = 29

    dims = {"courses": courses, "times": times, "teachers": teachers}

    # prefs = np.random.randint(7, size=(teachers, times, courses), dtype=np.uint64)
    prefs = np.loadtxt("formatted_prefs.csv", delimiter=",")
    loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
    max_iter = 2500
    P = np.array([0, 1, 2, 3, 4, 5, 6], dtype=np.uint64)
    p_tgt = 3

    hg = HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)
    hg.solve()
    
    assignments = []
    for key, _ in hg.sparse().items():
        assignments.append([num.item() for num in key])
        
    return {
        "assignments": list(assignments),
        "valid" : hg.is_valid_schedule()
    }

@app.post(
    "/schedule/validate",
    response_model=IsValidSchedule,
    responses={"400": {"model": Error}},
    tags=["algorithm1"],
)
def validate_schedule(body: Schedule = None) -> Union[IsValidSchedule, Error]:
    """
    Algorithm 1 endpoint to validate an existing schedule
    """
    courses = 33
    times = 51
    teachers = 29

    dims = {"courses": courses, "times": times, "teachers": teachers}

    # prefs = np.random.randint(7, size=(teachers, times, courses), dtype=np.uint64)
    prefs = np.loadtxt("formatted_prefs.csv", delimiter=",")
    loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
    max_iter = 2500
    P = np.array([0, 1, 2, 3, 4, 5, 6], dtype=np.uint64)
    p_tgt = 3

    hg = HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)
    hg.solve()

    return {"valid": hg.is_valid_schedule()}
'''

#'''
@serve.deployment(route_prefix="/schedule")
@serve.ingress(app)
class Algorithm1:
    @app.post(
        "/create",
        response_model=Schedule,
        responses={"400": {"model": Error}},
        tags=["algorithm1"],
    )
    def create_schedule(body: InputData = None) -> Union[Schedule, Error]:
        """
        Algorithm 1 endpoint to generate a schedule
        """
        courses = 33
        times = 51
        teachers = 29

        dims = {"courses": courses, "times": times, "teachers": teachers}

        prefs = np.loadtxt("formatted_prefs.csv", delimiter=",")
        loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
        max_iter = 2500
        P = np.array([0, 1, 2, 3, 4, 5, 6], dtype=np.uint64)
        p_tgt = 3

        assignments = []
        for key, _ in hg.sparse().items():
            assignments.append([num.item() for num in key])
        
        return {
            "assignments": list(assignments),
            "valid" : hg.is_valid_schedule()
        }

    @app.post(
        "/validate",
        response_model=IsValidSchedule,
        responses={"400": {"model": Error}},
        tags=["algorithm1"],
    )
    def validate_schedule(body: Schedule = None) -> Union[IsValidSchedule, Error]:
        """
        Algorithm 1 endpoint to validate an existing schedule
        """
        courses = 33
        times = 51
        teachers = 29

        dims = {"courses": courses, "times": times, "teachers": teachers}

        prefs = np.random.randint(7, size=(teachers, times, courses), dtype=np.uint64)
        loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
        max_iter = 2500
        P = np.array([0, 1, 2, 3, 4, 5, 6], dtype=np.uint64)
        p_tgt = 3

        hg = HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)
        hg.solve()

        return {"valid": hg.is_valid_schedule()}

deployment_graph = Algorithm1.bind()
#'''
