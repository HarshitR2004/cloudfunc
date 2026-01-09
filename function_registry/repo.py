
from sqlalchemy.orm import Session
from models import Function

def register_function(
    db: Session,
    name: str,
    image: str,
    runtime: str
):
    fn = Function(
        name=name,
        image=image,
        runtime=runtime
    )
    db.add(fn)
    db.commit()
    db.refresh(fn)
    return fn

def get_function(db: Session, name: str):
    return db.query(Function).filter(Function.name == name).first()

def update_warm_status(db: Session, name: str, is_warm: bool):
    fn = get_function(db, name)
    if fn:
        fn.is_warm = is_warm
        db.commit()
    return fn

def update_last_invoked(db: Session, name: str):
    fn = get_function(db, name)
    if fn:
        fn.last_invoked_at = func.now()
        db.commit()