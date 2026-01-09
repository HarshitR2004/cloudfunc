from pydantic import BaseModel

class DeployRequest(BaseModel):
    name: str
    image: str
    runtime: str

class InvokeRequest(BaseModel):
    payload: dict
