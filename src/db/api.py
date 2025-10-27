
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from db import crud, database, schemas
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def root():
    return {"message": "API is running"}


@router.get("/tasks", response_model=list[schemas.TaskResponse])
def list_tasks(db : Session = Depends(get_db), query: str | None = None, completed: bool | None = None):
    #Need to add custom 400 checks for query params?

    return crud.get_tasks(db=db, query=query, completed=completed)


@router.post("/tasks", status_code=201, response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    print("Parsed task object:", task)
    print("due_date type:", type(task.due_date))
    return crud.create_task(db=db, task=task)

@router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated = crud.update_task(db=db, task_id=task_id, task=task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None