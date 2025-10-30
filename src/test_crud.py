"""
Domain tests for CRUD operations.
These tests cover the basic Create, Read, Update, and Delete functionalities
for tasks in the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import crud, schemas, tables
from datetime import datetime

TEST_DB_URL = "sqlite:///./test_unimicro.db"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)
tables.Task.__table__.drop(bind=engine, checkfirst=True)
tables.Base.metadata.create_all(bind=engine)


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_task():
    db = next(get_test_db())
    task_data = schemas.TaskCreate(
        title="Test Task",
        tags="test,unit",
        completed=False,
        due_date=datetime(2024, 12, 31, 23, 59)
    )
    created_task = crud.create_task(db, task_data)
    assert created_task.id is not None
    assert created_task.title == "Test Task"
    assert created_task.tags == "test,unit"
    assert created_task.completed is False
    assert created_task.due_date == datetime(2024, 12, 31, 23, 59)



def test_get_tasks():
    db = next(get_test_db())
    tasks = crud.get_tasks(db)
    assert len(tasks) >= 1


def test_update_task():
    db = next(get_test_db())
    tasks = crud.get_tasks(db)
    task_to_update = tasks[0]

    update_data = schemas.TaskUpdate(
        title="Updated Test Task",
        tags="updated,unit",
        completed=True
    )
    updated_task = crud.update_task(db, task_to_update.id, update_data)
    assert updated_task.title == "Updated Test Task"
    assert updated_task.tags == "updated,unit"
    assert updated_task.completed is True

def test_delete_task():
    db = next(get_test_db())
    tasks = crud.get_tasks(db)
    task_to_delete = tasks[0]

    success = crud.delete_task(db, task_to_delete.id)
    assert success is True

    deleted_task = crud.get_task(db, task_to_delete.id)
    assert deleted_task is None

if __name__ == "__main__":
    test_create_task()
    test_get_tasks()
    test_update_task()
    test_delete_task()
