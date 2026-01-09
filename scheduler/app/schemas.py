from pydantic import BaseModel

class ScheduleRequest(BaseModel):
    function: str
    payload: dict