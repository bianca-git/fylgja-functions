# functions/main.py

from firebase_functions import https_fn
from flask import Request, Response
import firebase_admin
from firebase_admin import firestore
from google.cloud import firestore as gcf
import json

_firebase_app = None
_firestore_db = None


def get_db():
    global _firebase_app, _firestore_db
    if _firebase_app is None or _firestore_db is None:
        _firebase_app = firebase_admin.initialize_app()
        _firestore_db = firestore.client()
    return _firestore_db


@https_fn.on_request()
def checkin(request: Request) -> Response:
    db = get_db()
    try:
        data = request.get_json()
        text = data.get("text", "")
        user_id = data.get("userId", "demo-user")
        # TODO: Integrate NLP here to extract tasks/status
        db.collection("checkins").add(
            {"userId": user_id, "text": text, "timestamp": gcf.SERVER_TIMESTAMP}
        )
        return Response(
            json.dumps({"message": "Check-in received"}),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}), status=400, mimetype="application/json"
        )


@https_fn.on_request()
def create_task(request: Request) -> Response:
    db = get_db()
    try:
        data = request.get_json()
        user_id = data.get("userId", "demo-user")
        task = {
            "userId": user_id,
            "taskDescription": data.get("taskDescription", ""),
            "status": data.get("status", "To-Do"),
            "dateCreated": gcf.SERVER_TIMESTAMP,
            "dateCompleted": None,
            "reminderTime": data.get("reminderTime"),
        }
        doc_ref = db.collection("tasks").add(task)
        return Response(
            json.dumps({"id": doc_ref[1].id, "message": "Task created"}),
            status=201,
            mimetype="application/json",
        )
    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}), status=400, mimetype="application/json"
        )


@https_fn.on_request()
def get_tasks(request: Request) -> Response:
    db = get_db()
    user_id = request.args.get("userId", "demo-user")
    tasks_ref = db.collection("tasks").where("userId", "==", user_id)
    tasks = []
    for doc in tasks_ref.stream():
        t = doc.to_dict()
        t["id"] = doc.id
        tasks.append(t)
    return Response(
        json.dumps({"tasks": tasks}), status=200, mimetype="application/json"
    )


@https_fn.on_request()
def mark_task_done(request: Request, task_id=None) -> Response:
    db = get_db()
    try:
        if not task_id:
            # fallback for local testing or if not provided
            task_id = request.path.split("/")[-2]
        task_ref = db.collection("tasks").document(task_id)
        task_ref.update({"status": "Done", "dateCompleted": gcf.SERVER_TIMESTAMP})
        return Response(
            json.dumps({"message": "Task marked as done"}),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}), status=400, mimetype="application/json"
        )


@https_fn.on_request()
def update_task(request: Request, task_id=None) -> Response:
    db = get_db()
    try:
        if not task_id:
            task_id = request.path.split("/")[-1]
        data = request.get_json()
        update_data = {}
        for field in ["taskDescription", "status", "reminderTime"]:
            if field in data:
                update_data[field] = data[field]
        if "status" in update_data and update_data["status"] == "Done":
            update_data["dateCompleted"] = gcf.SERVER_TIMESTAMP
        task_ref = db.collection("tasks").document(task_id)
        task_ref.update(update_data)
        return Response(
            json.dumps({"message": "Task updated"}),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}), status=400, mimetype="application/json"
        )


@https_fn.on_request()
def get_summary(request: Request) -> Response:
    db = get_db()
    user_id = request.args.get("userId", "demo-user")
    try:
        tasks_ref = db.collection("tasks").where("userId", "==", user_id)
        done = 0
        todo = 0
        for doc in tasks_ref.stream():
            t = doc.to_dict()
            if t.get("status") == "Done":
                done += 1
            else:
                todo += 1
        summary = {
            "done": done,
            "todo": todo,
            "message": f"You have completed {done} tasks. {todo} still to do!",
        }
        return Response(
            json.dumps({"summary": summary}), status=200, mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}), status=400, mimetype="application/json"
        )
