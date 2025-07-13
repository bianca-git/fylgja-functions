import firebase_admin
from firebase_admin import credentials, firestore
import datetime

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)
db = firestore.client()

# Seed demo user
db.collection("users").document("demo-user").set(
    {"displayName": "Demo User", "created": datetime.datetime.utcnow()}
)

# Seed demo tasks
db.collection("tasks").add(
    {
        "userId": "demo-user",
        "taskDescription": "Finish the board presentation",
        "status": "Done",
        "dateCreated": datetime.datetime.utcnow(),
        "dateCompleted": datetime.datetime.utcnow(),
    }
)
db.collection("tasks").add(
    {
        "userId": "demo-user",
        "taskDescription": "Book dentist appointment",
        "status": "To-Do",
        "dateCreated": datetime.datetime.utcnow(),
    }
)

print("Seed data added.")
