from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
import models

# Shared Task Properties
class TaskBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    status: Optional[models.StatusEnum] = models.StatusEnum.pending

# Properties to explicitly receive on task creation
class TaskCreate(TaskBase):
    pass

# Properties to return to client
class Task(TaskBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Shared User Properties
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr

# Properties to explicitly receive on user creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role: Optional[models.RoleEnum] = models.RoleEnum.user

# Properties to return to client
class User(UserBase):
    id: int
    role: models.RoleEnum
    created_at: datetime

    class Config:
        from_attributes = True

# JWT Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TokenData(BaseModel):
    email: Optional[str] = None
