from fastapi import APIRouter
from app.schemas.function import DeployRequest
from app.registry_client import register_function

router = APIRouter()

@router.post("/deploy")
def deploy_function(data: DeployRequest):
    register_function(data)
    return {"message": "Function deployed"}