# Fylgja Check-in Bot

Fylgja is a simple check-in and task management bot built on Firebase Cloud Functions and Firestore. It provides a basic web interface for users to submit daily check-ins and manage their tasks.

## Project Structure

- `functions/`: Contains the Python-based Firebase Cloud Functions.
  - `main.py`: The main application file with all the cloud function definitions.
  - `requirements.txt`: Python dependencies for the functions.
  - `firestore.rules`: Security rules for the Firestore database.
- `web/`: The frontend of the application.
  - `index.html`: The main HTML file for the user interface.
  - `app.js`: JavaScript for handling user interactions and API calls.
  - `style.css`: CSS for styling the web interface.
- `public/`: Default Firebase hosting directory.
- `firebase.json`: Configuration for Firebase services.
- `.github/workflows/deploy.yml`: GitHub Actions workflow for continuous deployment.

## Features

- **Daily Check-ins:** Users can submit daily updates on their work.
- **Task Management:** Users can create, view, update, and mark tasks as done.
- **Summaries:** Users can view a summary of their completed and pending tasks.

## Setup and Deployment

1.  **Prerequisites:**
    - Python 3.13
    - Node.js (for Firebase CLI)
    - Firebase CLI

2.  **Installation:**
    - Clone the repository.
    - Install Python dependencies: `pip install -r functions/requirements.txt`
    - Install Firebase CLI: `npm install -g firebase-tools`

3.  **Local Development:**
    - Run the Firebase emulators: `firebase emulators:start`
    - The functions and web interface will be available locally.

4.  **Deployment:**
    - Pushing to the `main` branch will automatically deploy the application to Firebase using the GitHub Actions workflow.

## Proposed Automated Testing Plan

To improve the reliability of the application and ensure new changes don't break existing functionality, we propose integrating automated testing into the CI/CD pipeline.

### 1. Testing Framework

We will use `pytest` for writing and running our tests. It's a popular and powerful testing framework for Python. We will also use the `requests` library to make HTTP requests to our functions during testing.

### 2. Test Structure

- Tests will be placed in a new `functions/tests/` directory.
- Test files will be named `test_*.py` (e.g., `test_main.py`).
- Each function in `main.py` will have a corresponding test function.

### 3. Example Test (for `get_tasks` function)

```python
# functions/tests/test_main.py
import requests

BASE_URL = "http://localhost:5001/fylgja/us-central1"

def test_get_tasks():
    response = requests.get(f"{BASE_URL}/get_tasks?userId=test-user")
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert isinstance(data["tasks"], list)
```

### 4. CI/CD Integration

The `.github/workflows/deploy.yml` file will be updated to include a new "Test" step before the "Deploy" step. This will ensure that tests are run automatically before any new code is deployed.

**Updated `.github/workflows/deploy.yml`:**

```yaml
name: Deploy to Firebase

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install Firebase CLI
        run: npm install -g firebase-tools

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Install Python dependencies
        run: |
          cd functions
          pip install -r requirements.txt
          pip install pytest requests

      - name: Run Tests
        run: |
          cd functions
          firebase emulators:start &
          sleep 10 # Wait for emulators to start
          pytest
          kill %1 # Kill the emulators

      - name: Build web UI (if needed)
        run: echo "No build step for plain HTML/JS"

      - name: Deploy to Firebase
        env:
          FIREBASE_TOKEN: ${{ secrets.FIREBASE_SECRET }}
        run: |
          echo '${{ secrets.FIREBASE_SECRET }}' > ${HOME}/gcloud.json
          firebase deploy --token "${{ secrets.FIREBASE_SECRET }}" --non-interactive
```

This new testing plan will provide a solid foundation for building a more robust and reliable application.
