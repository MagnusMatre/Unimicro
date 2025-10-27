from ctypes import Array
import datetime
from narwhals import String
from sqlalchemy.orm import Session
from . import tables
from db import schemas, tables
from sqlalchemy import or_


def get_task(db: Session, task_id: int):
    return db.query(tables.Task).filter(tables.Task.id == task_id).first()

def get_tasks(db: Session,  query: str = "", completed: bool | None = None):
    q = db.query(tables.Task)
    if query:
        q = q.filter(or_(
            tables.Task.title.ilike(f"%{query}%"),
            tables.Task.tags.ilike(f"%{query}%")
        ))
    if completed is not None:
        q = q.filter(tables.Task.completed == completed)
    return q.all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = tables.Task(**task.dict())
    db_task.created_at = datetime.datetime.now()
    db_task.updated_at = datetime.datetime.now()    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    # Update only fields provided
    if task.title is not None:
        db_task.title = task.title
    if task.tags is not None:
        db_task.tags = task.tags
    if task.completed is not None:
        db_task.completed = task.completed
    if task.due_date is not None:
        db_task.due_date = task.due_date

    # Always update the timestamp
    db_task.updated_at = datetime.datetime.now()

    db.commit()
    db.refresh(db_task)

    return db_task
def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True

def get_tasks_filtered(db: Session, query: str | None = None, completed: bool | None = None):
    q = db.query(tables.Task)
    if query:
        q = q.filter(tables.Task.title.contains(query) | tables.Task.description.contains(query))
    if completed is not None:
        q = q.filter(tables.Task.completed == (1 if completed else 0))
    return q.all()

