from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    username: str
    password: str

class UserCreate(UserBase):
    role: str
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None

class UserUpdate(UserBase):
    email: Optional[str]
    username: Optional[str]
    password: Optional[str]
    updated_at: Optional[datetime] = datetime.now()

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    role: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
class UserGetMeResponse(BaseModel):
    id: str
    email: str
    username: str
    role: str
    exp: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
class UserLogin(BaseModel):
    username: str
    password: str

class UserLoginResponse(BaseModel):
    result: dict
    # result: dict

class UserDeleteResponse(BaseModel):
    message: str