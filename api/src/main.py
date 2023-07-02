from __future__ import annotations
from fastapi import FastAPI
from typing import Union
from models import Success, Error, InputData, IsValidSchedule, Schedule
from hypergraph import HyperGraph
from search_drivers import distributed_driver, sequential_driver



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


@app.post(
    "/schedule/create",
    response_model=Schedule,
    responses={"400": {"model": Error}},
    tags=["algorithm1"],
)
def create_schedule(input_data: InputData = None) -> Union[Schedule, Error]:
    """
    Algorithm 1 endpoint to generate a schedule
    """
    result = distributed_driver(input_data)
    
    match result:
        case None:
            return Schedule(
                assignments = [],
                valid = False,
                complete = False
            )
        
        case HyperGraph(): 
            return Schedule(
                assignments = list(result.sparse_tensor.keys()), 
                valid = result.is_valid_schedule(),
                complete = result.is_complete()
            )
        
        case _:
            return Error(
               message = "RuhRohRaggy"
            )


@app.post(
    "/schedule/validate",
    response_model=IsValidSchedule,
    responses={"400": {"model": Error}},
    tags=["algorithm1"],
)
def validate_schedule(schedule: Schedule = None) -> Union[IsValidSchedule, Error]:
    """
    Algorithm 1 endpoint to validate an existing schedule
    """
    result = sequential_driver()
    
    match result:
        case None:
            return IsValidSchedule(
                valid = False
            )
        
        case HyperGraph(): 
            return IsValidSchedule(
                valid = result.is_valid_schedule()
            )

        case _:
            return Error(
               message = "RuhRohRaggy"
            )
