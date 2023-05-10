from fastapi import FastAPI, Response, Depends, status, HTTPException
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

@app.post("/todo/", status_code=status.HTTP_201_CREATED)
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

@app.get("/todo/{id}", status_code=200)
def show(id, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo with the id {id} is not available")
        
    return todo
    