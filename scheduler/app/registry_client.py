from sqlalchemy.orm import Session
from function_registry.db import SessionLocal
from function_registry.repo import get_function

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fetch_function(name: str):
    db = SessionLocal()
    try:
        return get_function(db, name)
    finally:
        db.close()
