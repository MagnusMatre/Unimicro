from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# Shared fields
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=140)
    tags: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = Field(default=False)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=140)
    tags: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 