from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, List

class TaskBase(BaseModel):
    title: str
    description: str
    deadline: date
    level: str
    category: str
    status: str

class TaskCreate(TaskBase):
    user_id: List[str] 
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None


class TaskUpdate(TaskBase):
    title: Optional[str]
    description: Optional[str]
    deadline: Optional[date]
    level: Optional[str]
    category: Optional[str]
    status: Optional[str]
    updated_at: Optional[datetime] = datetime.now()

class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    deadline: date
    level: str
    category: str
    status: str
    user_id: List[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class TaskDeleteResponse(BaseModel):
    message: str