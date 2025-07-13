# functions/main.py
from firebase_functions import https_fn
from flask import Request, Response
import firebase_admin
from firebase_admin import firestore
from google.cloud import firestore as gcf
import json
import datetime

_firebase_app = None
_firestore_db = None


def get_db():
    global _firebase_app, _firestore_db
    if _firebase_app is None or _firestore_db is None:
        _firebase_app = firebase_admin.initialize_app()
        _firestore_db = firestore.client()
    return _firestore_db


# --- Endpoint: Submit Check-in ---
@https_fn.on_request()
def checkin(request: Request) -> Response:
    db = get_db()
    data = request.get_json()
    text = data.get("text", "")
    user_id = "demo-user"  # Replace with real user auth in production
    # TODO: Integrate NLP here to extract tasks/status
    db.collection("checkins").add(
        {"userId": user_id, "text": text, "timestamp": gcf.SERVER_TIMESTAMP}
    )
    return Response("Check-in received", status=200)


# --- Endpoint: Get Tasks ---
@https_fn.on_request()
def get_tasks(request: Request) -> Response:
    db = get_db()
    user_id = "demo-user"
    tasks_ref = db.collection("tasks").where("userId", "==", user_id)
    tasks = []
    for doc in tasks_ref.stream():
        t = doc.to_dict()
        t["id"] = doc.id
        tasks.append(t)
    return Response(
        json.dumps({"tasks": tasks}), status=200, mimetype="application/json"
    )


# --- Endpoint: Mark Task Done ---
@https_fn.on_request()
def mark_task_done(request: Request) -> Response:
    db = get_db()
    task_id = request.path.split("/")[-2]
    task_ref = db.collection("tasks").document(task_id)
    task_ref.update({"status": "Done", "dateCompleted": datetime.datetime.utcnow()})
    return Response("Task marked as done", status=200)


# --- Endpoint: Get Summary ---
@https_fn.on_request()
def get_summary(request: Request) -> Response:
    db = get_db()
    user_id = "demo-user"
    # Simple summary: count done/to-do
    tasks_ref = db.collection("tasks").where("userId", "==", user_id)
    done = 0
    todo = 0
    for doc in tasks_ref.stream():
        t = doc.to_dict()
        if t.get("status") == "Done":
            done += 1
        else:
            todo += 1
    summary = f"You have completed {done} tasks. {todo} still to do!"
    return Response(
        json.dumps({"summary": summary}), status=200, mimetype="application/json"
    )
