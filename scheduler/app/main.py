from fastapi import FastAPI, HTTPException
from app.schemas import ScheduleRequest
from app.queue import publish_invocation
from app.registry_client import fetch_function

app = FastAPI(title="CloudFunc Scheduler")

@app.post("/schedule")
def schedule(req: ScheduleRequest):
    fn = fetch_function(req.function)

    if not fn:
        raise HTTPException(
            status_code=404,
            detail="Function not registered"
        )

    publish_invocation({
        "function": req.function,
        "payload": req.payload
    })

    return {
        "message": "Invocation scheduled",
        "function": req.function,
        "warm": fn["is_warm"]
    }

@app.get("/health")
def health():
    return {"status": "scheduler-ok"}


