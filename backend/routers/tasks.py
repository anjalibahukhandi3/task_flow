from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
import models, schemas, database
from .. import auth


router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)

@router.get("", response_model=dict)
def read_tasks(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
) -> Any:
    # Admins get all tasks, users get their own
    if current_user.role == models.RoleEnum.admin:
        tasks = db.query(models.Task).all()
    else:
        tasks = db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
        
    # Serialize to match expected frontend structure
    task_data = []
    for t in tasks:
        # Pre-load user relation if admin
        user_info = None
        if current_user.role == models.RoleEnum.admin and t.owner:
            user_info = {"name": t.owner.name, "email": t.owner.email}
            
        task_data.append({
            "_id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status.value,
            "user": user_info or t.user_id,
            "createdAt": t.created_at.isoformat() if t.created_at else None
        })
        
    return {
        "success": True,
        "count": len(task_data),
        "data": task_data
    }

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
) -> Any:
    db_task = models.Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        user_id=current_user.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return {
        "success": True,
        "data": {
            "_id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "status": db_task.status.value
        }
    }

@router.get("/{id}", response_model=dict)
def read_task(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
) -> Any:
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    if task.user_id != current_user.id and current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
        
    return {"success": True, "data": task}

@router.put("/{id}", response_model=dict)
def update_task(
    id: int,
    task_in: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
) -> Any:
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    if task.user_id != current_user.id and current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
        
    task.title = task_in.title
    task.description = task_in.description
    task.status = task_in.status
    
    db.commit()
    db.refresh(task)
    
    return {"success": True, "data": {"_id": task.id, "title": task.title, "description": task.description, "status": task.status.value}}

@router.delete("/{id}", response_model=dict)
def delete_task(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
) -> Any:
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    if task.user_id != current_user.id and current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
        
    db.delete(task)
    db.commit()
    
    return {"success": True, "data": {}}
