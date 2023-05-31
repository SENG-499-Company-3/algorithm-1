from pydantic import BaseModel


class Schedule(BaseModel):
    assignments: dict
    is_valid: bool
