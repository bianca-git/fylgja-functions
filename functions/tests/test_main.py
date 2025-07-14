# functions/tests/test_main.py
import requests

BASE_URL = "http://127.0.0.1:5001/fylgja-functions/us-central1"

def test_get_tasks():
    response = requests.get(f"{BASE_URL}/get_tasks?userId=test-user")
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert isinstance(data["tasks"], list)

def test_create_task():
    response = requests.post(f"{BASE_URL}/create_task", json={"taskDescription": "Test task"})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "message" in data

def test_mark_task_done():
    # First, create a task to mark as done
    create_response = requests.post(f"{BASE_URL}/create_task", json={"taskDescription": "Test task for marking done"})
    task_id = create_response.json()["id"]

    # Now, mark it as done
    response = requests.post(f"{BASE_URL}/mark_task_done", json={"taskId": task_id})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task marked as done"

def test_update_task():
    # First, create a task to update
    create_response = requests.post(f"{BASE_URL}/create_task", json={"taskDescription": "Test task for updating"})
    task_id = create_response.json()["id"]

    # Now, update it
    update_data = {"taskId": task_id, "taskDescription": "Updated task description"}
    response = requests.post(f"{BASE_URL}/update_task", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task updated"
