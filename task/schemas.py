from pydantic import BaseModel

class Todo(BaseModel):
    title: str
    body: str
    

class User(BaseModel):
    name: str
    email: str
    password: str
    