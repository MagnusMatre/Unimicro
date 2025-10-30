
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from db import crud, database, schemas, tables
from sqlalchemy.orm import Session
from db.authentication import hash_password, verify_password

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


@router.get("/tasks/{username}/{task_id}", response_model=schemas.TaskResponse)
def read_task(username, task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(username, db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/tasks/{username}", response_model=list[schemas.TaskResponse])
def list_tasks(username : str, db : Session = Depends(get_db), query: str | None = None, completed: bool | None = None):
    return crud.get_tasks(username = username, db=db, query=query, completed=completed)


@router.post("/tasks/{username}", status_code=201, response_model=schemas.TaskResponse)
def create_task(username, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(username=username,db=db, task=task)

@router.put("/tasks/{username}/{task_id}", response_model=schemas.TaskResponse)
def update_task(username, task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated = crud.update_task(username,db=db, task_id=task_id, task=task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/tasks/{username}/{task_id}", status_code=204)
def delete_task(username, task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(username, db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None

@router.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(tables.User).filter(tables.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if crud.create_user(db, user):
        return JSONResponse(content={"message": "User registered"}, status_code=status.HTTP_201_CREATED)

@router.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    if crud.authenticate_user(db, user.username, user.password):
        return JSONResponse(content={"message": "Login successful"}, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    

"""
NB!!! This is only for testing purposes and should be removed or protected in production.
"""
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users