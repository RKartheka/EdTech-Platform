
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str  # "student" or "teacher"

class UserLogin(BaseModel):
    email: str
    password: str

class AssignmentCreate(BaseModel):
    title: str
    description: Optional[str]
    due_date: Optional[str]

class AssignmentOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    due_date: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class SubmissionCreate(BaseModel):
    content: str

class SubmissionOut(BaseModel):
    id: int
    content: str
    submitted_at: datetime
    student_id: int

    class Config:
        orm_mode = True
