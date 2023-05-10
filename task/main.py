from fastapi import FastAPI, HTTPException, Depends
from typing import Optional 
import schemas, models
from typing import List
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todo/")
def create(request: schemas.Todo, db: Session = Depends(get_db)):
    new_todo = models.Todo(title=request.title, body=request.body)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.get("/todo/")
def all(db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return todos