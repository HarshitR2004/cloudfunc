from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from repo import register_function, get_function, update_warm_status

app = FastAPI(title="Function Registry")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/functions")
def create_function(data: dict):
    db = SessionLocal()
    try:
        fn = register_function(
            db,
            name=data["name"],
            image=data["image"],
            runtime=data["runtime"]
        )
        return {"name": fn.name}
    except Exception:
        raise HTTPException(status_code=400, detail="Function exists")

@app.get("/functions/{name}")
def fetch_function(name: str):
    db = SessionLocal()
    fn = get_function(db, name)
    if not fn:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "name": fn.name,
        "image": fn.image,
        "runtime": fn.runtime,
        "is_warm": fn.is_warm
    }

    
