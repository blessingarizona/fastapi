from fastapi import APIRouter, Depends
from typing import list
from . import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/todo/")
def all(db: Session = Depends(database.get_db)):
    todos = db.query(models.Todo).all()
    return todos