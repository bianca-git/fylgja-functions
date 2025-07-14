import subprocess
import time
import requests
import os

def run_tests():
    # Start the functions-framework server
    server = subprocess.Popen(["functions-framework", "--source", "main.py", "--port", "5001"], cwd=os.path.dirname(os.path.abspath(__file__)))
    time.sleep(2)  # Give the server a moment to start

    # Run the tests
    try:
        # Test get_tasks
        response = requests.get("http://127.0.0.1:5001/get_tasks?userId=test-user")
        assert response.status_code == 200
        print("test_get_tasks passed")

        # Test create_task
        response = requests.post("http://127.0.0.1:5001/create_task", json={"taskDescription": "Test task"})
        assert response.status_code == 201
        print("test_create_task passed")

        # Test mark_task_done
        create_response = requests.post("http://127.0.0.1:5001/create_task", json={"taskDescription": "Test task for marking done"})
        task_id = create_response.json()["id"]
        response = requests.post("http://127.0.0.1:5001/mark_task_done", json={"taskId": task_id})
        assert response.status_code == 200
        print("test_mark_task_done passed")

        # Test update_task
        create_response = requests.post("http://127.0.0.1:5001/create_task", json={"taskDescription": "Test task for updating"})
        task_id = create_response.json()["id"]
        update_data = {"taskId": task_id, "taskDescription": "Updated task description"}
        response = requests.post("http://127.0.0.1:5001/update_task", json=update_data)
        assert response.status_code == 200
        print("test_update_task passed")

    finally:
        # Stop the server
        server.terminate()

if __name__ == "__main__":
    run_tests()