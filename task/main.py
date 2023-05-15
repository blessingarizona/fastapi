from fastapi import FastAPI, Response, Depends, status, HTTPException
from typing import Optional 
import schemas, models
from typing import List
from database import engine, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from routers import authentication


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

db = []

@app.post("/todo/")
def create(request: schemas.Todo, db: Session = Depends(get_db)):
    new_todo = models.Todo(title=request.title, body=request.body)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# @app.get("/todo/")
# def all(db: Session = Depends(get_db)):
#     todos = db.query(models.Todo).all()
#     return todos

@app.get("/todo/{id}", status_code=200)
def show(id, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo with the id {id} is not available")
        
    return todo

@app.put("/todo/{id}", status_code=200)
def update(id, request: schemas.Todo, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id)
    if not todo.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Todo with id {id} not found")
    todo.update(request)
    db.commit()
    return 'updated'

@app.delete("/todo/{id}", status_code=200)
def destory(id, db: Session = Depends(get_db)):
    db.query(models.Todo).filter(models.Todo.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'
    
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/user/")
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(name=request.name,email=request.email,password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
app.include_router(authentication.router)
    