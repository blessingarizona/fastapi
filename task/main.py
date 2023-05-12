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

db = []

@app.post("/todo/")
async def create_todo(todo: schemas.Todo, db: Session = Depends(get_db)):
    db.Depends(todo)
    return todo

@app.get("/todo/", response_model=List[schemas.Todo])
async def get_all_todos(todo: schemas.Todo, db: Session = Depends(get_db)):
    return db

@app.get("/todo/done", response_model=List[schemas.Todo])
async def get_done_todos(todo: schemas.Todo, db: Session = Depends(get_db)):
    return [todo for todo in db if todo.done]

@app.get("/todo/{id}")
async def get_todo(id: int):

    try:
        return db[id]
    except:
       raise HTTPException (status_code=404, detail="Todo not Found")

@app.put("/todo/{id}")
async def update_todo(id: int, todo: schemas.Todo):
    
    try:

        db[id] = todo
        return db[id]

    except:

        raise HTTPException(status_code=404, detail="Todo Not Found")


@app.delete("/todo/{id}")
async def delete_todo(id: int):

    try:

        obj = db[id]
        db.pop(id)
        return obj

    except:

        raise HTTPException(status_code=404, detail="Todo Not Found")


    