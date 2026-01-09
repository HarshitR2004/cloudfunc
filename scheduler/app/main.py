from fastapi import FastAPI
from app.schemas import ScheduleRequest
from app.queue import publish_invocation
from app.registry_client import fetch_function

app = FastAPI(title="CloudFunc Scheduler")

@app.post("/schedule")
def schedule(req: ScheduleRequest):
    fn = fetch_function(req.function)

    if not fn:
        return {"error": "Function not found"}  # defensive

    # Phase 4: always enqueue
    publish_invocation({
        "function": req.function,
        "payload": req.payload
    })

    return {
        "message": "Invocation scheduled",
        "function": req.function
    }

@app.get("/health")
def health():
    return {"status": "scheduler-ok"}

