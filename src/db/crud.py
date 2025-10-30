from ctypes import Array
import datetime
from narwhals import String
from sqlalchemy.orm import Session
from . import tables
from db import schemas, tables
from sqlalchemy import or_
from db.authentication import hash_password, verify_password

def get_task(username, db: Session, task_id: int):
    return db.query(tables.Task).filter(tables.Task.created_by == username).filter(tables.Task.id == task_id).first()

def get_tasks(username, db: Session,  query: str = "", completed: bool | None = None):
    q = db.query(tables.Task).filter(tables.Task.created_by == username)
    if query:
        q = q.filter(or_(
            tables.Task.title.ilike(f"%{query}%"),
            tables.Task.tags.ilike(f"%{query}%")
        ))
    if completed is not None:
        q = q.filter(tables.Task.completed == completed)
    return q.all()

def create_task(username, db: Session, task: schemas.TaskCreate):
    db_task = tables.Task(**task.dict())
    db_task.created_by = username
    db_task.updated_by = username
    db_task.created_at = datetime.datetime.now()
    db_task.updated_at = datetime.datetime.now()    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(username, db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = get_task(username, db, task_id)
    if not db_task:
        return None
    
    if task.title is not None:
        db_task.title = task.title
    if task.tags is not None:
        db_task.tags = task.tags
    if task.completed is not None:
        db_task.completed = task.completed
    if task.due_date is not None:
        db_task.due_date = task.due_date

    db_task.updated_at = datetime.datetime.now()
    db_task.updated_by = username

    db.commit()
    db.refresh(db_task)

    return db_task

def delete_task(username, db: Session, task_id: int):
    task = get_task(username,db, task_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True

def get_tasks_filtered(username, db: Session, query: str | None = None, completed: bool | None = None):
    q = db.query(tables.Task).filter(tables.Task.created_by == username)
    if query:
        q = q.filter(tables.Task.title.contains(query) | tables.Task.description.contains(query))
    if completed is not None:
        q = q.filter(tables.Task.completed == (1 if completed else 0))
    return q.all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = tables.User(username=user.username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True

def authenticate_user(db: Session, username: str, password: str):
    db_user = db.query(tables.User).filter(tables.User.username == username).first()
    if not db_user:
        return False
    if not verify_password(password, db_user.password_hash):
        return False
    return True

"""
NB!!! This is only for testing purposes, should be removed or protected in production.
"""
def get_users(db: Session):
    return db.query(tables.User).all()
