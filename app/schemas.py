from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    completed: Optional[bool]

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        from_attributes = True