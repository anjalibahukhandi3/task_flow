from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any
import models, schemas, database
from .. import auth


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)) -> Any:
    # Check if user exists
    user_exists = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user_exists:
        return {
            "success": False,
            "error": "User with this email already exists."
        }

    
    # Hash password and save
    hashed_password = auth.get_password_hash(user_in.password)
    db_user = models.User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate token
    access_token = auth.create_access_token(data={"sub": db_user.email})
    
    return {
        "success": True,
        "token": access_token,
        "role": db_user.role.value
    }

# We use the same schema the Node.js frontend sends for login ({email, password} JSON body rather than OAuth2 form)
from pydantic import BaseModel
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=dict)
def login_user(login_data: LoginRequest, db: Session = Depends(database.get_db)) -> Any:
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    if not user or not auth.verify_password(login_data.password, user.hashed_password):
        return {
            "success": False,
            "error": "Incorrect email or password"
        }

    
    access_token = auth.create_access_token(data={"sub": user.email})
    
    return {
        "success": True,
        "token": access_token,
        "role": user.role.value
    }

@router.get("/me", response_model=dict)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return {
        "success": True,
        "data": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role.value
        }
    }
