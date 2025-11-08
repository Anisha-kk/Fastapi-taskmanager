# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError,jwt
from sqlalchemy.orm import Session
from typing import List
import os
from enum import Enum
import random
from app.models import task as task_model
from app.models import user as user_model
from app.schemas import task as task_schema
from app.schemas import user as user_schema
from app.db.session import get_db
from app.core.security import SECRET_KEY,ALGORITHM,oauth2_scheme
from logger.logger import Logger

info_logger = Logger.logger("infoLogger")

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

# Auth dependency
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: no username",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Create Task
@router.post("/", response_model=task_schema.TaskOut)
def create_task(task: task_schema.TaskCreate, db: Session = Depends(get_db), username=Depends(get_current_user)):
    info_logger.info("Creating New task") 
    new_task = task_model.Task(**task.dict(), ownername=username,id=random.randint(1000, 9999))
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    info_logger.info("New task created")
    return new_task

# Read all tasks for current user
@router.get("/", response_model=List[task_schema.TaskOut])
def read_tasks(db: Session = Depends(get_db), username=Depends(get_current_user)):
    info_logger.info("Read all tasks")
    tasks = db.query(task_model.Task).filter(task_model.Task.ownername == username).all()
    return tasks

# Read single task
@router.get("/{task_id}", response_model=task_schema.TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db), username=Depends(get_current_user)):
    info_logger.info(f"Read task {task_id}")
    task = db.query(task_model.Task).filter(task_model.Task.id == task_id, task_model.Task.ownername == username).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Delete Task
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), username=Depends(get_current_user)):
    info_logger.info(f"Delete task {task_id}")
    task = db.query(task_model.Task).filter(task_model.Task.id == task_id, task_model.Task.ownername == username).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    info_logger.info(f"Deleted task {task_id}")
    return None


#Update Task
@router.patch("/{task_id}")
def update_task(task_id: int,  task: task_schema.TaskUpdate,db: Session = Depends(get_db), username=Depends(get_current_user)):
    info_logger.info(f"Update task {task_id}")
    update_task = db.query(task_model.Task).filter(task_model.Task.id == task_id, task_model.Task.ownername == username).first()
    if not update_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.title is not None:
        update_task.title = task.title
    if task.description is not None:
        update_task.description = task.description
    if task.status is not None:
        update_task.status = task.status
    if task.priority is not None:
        update_task.priority = task.priority
    if task.due_date is not None:
        update_task.due_date = task.due_date
    
    db.commit()
    info_logger.info(f"Updated task {task_id}")
    return update_task
