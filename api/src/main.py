from __future__ import annotations
from fastapi import FastAPI
from typing import Union
from models import Success, Error, InputData, IsValidSchedule, Schedule
from hypergraph import HyperGraph
from drivers import validate_driver
from parse import parse
from generate_schedule import generate_schedule
from mock_input_data import MOCK_INPUT_DATA
from mock_schedule import MOCK_VALID_SCHEDULE


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
def create_schedule(input_data: InputData = MOCK_INPUT_DATA) -> Union[Schedule, Error]:
    """
    Algorithm 1 endpoint to generate a schedule
    """
    parse(input_data)
    result = generate_schedule(input_data)

    match result:
        case None:
            return Schedule(
                iterations=input_data.max_iter,
                valid=False,
                complete=False,
                c_hat=0.0,
                reward=0.0,
                quality=0.0,
                assignments=[],
                inputData=input_data
            )

        case Schedule():
            return result

        case _:
            return Error(
                message="RuhRohRaggy"
            )


@app.post(
    "/schedule/validate",
    response_model=IsValidSchedule,
    responses={"400": {"model": Error}},
    tags=["algorithm1"],
)
def validate_schedule(schedule: Schedule = MOCK_VALID_SCHEDULE) -> Union[IsValidSchedule, Error]:
    """
    Algorithm 1 endpoint to validate an existing schedule
    """
    result = validate_driver(schedule)

    match result:
        case None:
            return IsValidSchedule(
                valid=False
            )

        case IsValidSchedule():
            return result

        case _:
            return Error(
                message="RuhRohRaggy"
            )
