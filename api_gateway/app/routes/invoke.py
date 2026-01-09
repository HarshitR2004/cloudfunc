from fastapi import APIRouter, HTTPException
from app.schemas.function import InvokeRequest
from app.registry_client import get_function
import requests
import os

router = APIRouter()

SCHEDULER_URL = os.getenv("SCHEDULER_URL", "http://scheduler:9000")

@router.post("/invoke/{function_name}")
def invoke_function(
    function_name: str,
    data: InvokeRequest,
):
    fn = get_function(function_name)
    if not fn:
        raise HTTPException(status_code=404, detail="Function not found")

    # Forward request to scheduler
    requests.post(
        f"{SCHEDULER_URL}/schedule",
        json={
            "function": function_name,
            "payload": data.payload
        }
    )

    return {
        "message": "Invocation request accepted",
        "function": function_name
    }
