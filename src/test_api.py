from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

def test_create_task():
    """Test POST /tasks/{username}"""
    response = client.post(
        "/tasks/testuser",
        json={
            "title": "Test Task",
            "tags": "unit,test",
            "due_date": "2025-12-31T23:59:00"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["tags"] == "unit,test"
    assert data["completed"] is False
    assert data["created_by"] == "testuser"
    print("Created task ID:", data["id"])


def test_get_tasks():
    """Test GET /tasks/{username}"""
    response = client.get("/tasks/testuser")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) >= 1
    assert "title" in tasks[0]
    print("Retrieved tasks:", tasks)


def test_update_task():
    """Test PUT /tasks/{username}/{task_id}"""
    get_response = client.get("/tasks/testuser")
    task_id = get_response.json()[0]["id"]

    response = client.put(
        f"/tasks/testuser/{task_id}",
        json={
            "title": "Updated Test Task",
            "completed": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Test Task"
    assert data["completed"] is True
    print("Updated task ID:", data["id"])


def test_delete_task():
    """Test DELETE /tasks/{username}/{task_id}"""
    get_response = client.get("/tasks/testuser")
    task_id = get_response.json()[0]["id"]

    delete_response = client.delete(f"/tasks/testuser/{task_id}")
    assert delete_response.status_code == 204

    verify_response = client.get(f"/tasks/testuser/{task_id}")
    assert verify_response.status_code == 404
    print("Deleted task ID:", task_id)

if __name__ == "__main__":
    test_create_task()
    test_get_tasks()
    test_update_task()
    test_delete_task()
