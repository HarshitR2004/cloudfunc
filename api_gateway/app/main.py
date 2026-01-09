from fastapi import FastAPI
from app.routes import deploy, invoke

app = FastAPI(title="CloudFunc API Gateway")

app.include_router(deploy.router)
app.include_router(invoke.router)

@app.get("/health")
def health():
    return {"status": "ok"}

