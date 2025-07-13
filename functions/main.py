# functions/main.py

# Import necessary Firebase libraries
import firebase_admin
from firebase_admin import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

# Import Cloud Functions and HTTP types
from firebase_functions import https_fn
from flask import Response, Request, Flask, request  # <-- Import Request, Flask, and request from flask

# --- Global variables for lazy initialization ---
_firebase_app = None
_firestore_db = None

# --- Cloud Function: Fylgja's Message Receiver ---


@https_fn.on_request(timeout_sec=300)
def receive_fylgja_message(request: Request) -> Response:  # <-- Use flask.Request
    """
    This function listens for incoming HTTP requests, acting as a webhook
    for messaging platforms like WhatsApp or Facebook Messenger.
    """
    global _firebase_app, _firestore_db

    # Lazy initialization: Only initialize if not already done
    if _firebase_app is None or _firestore_db is None:
        try:
            _firebase_app = firebase_admin.initialize_app()
            _firestore_db = firestore.client()
            print("Firebase App and Firestore client initialized successfully.")
        except Exception as e:
            print(f"ERROR: Failed to initialize Firebase app or Firestore client: {e}")
            return Response("Internal Server Error during initialization", status=500)

    db = _firestore_db
    if db is None:
        print("ERROR: Firestore client is not initialized.")
        return Response(
            "Internal Server Error: Firestore client not initialized", status=500
        )

    print("----- Fylgja Received a Message! -----")
    print(f"Request Method: {request.method}")
    print(f"Request Headers: {request.headers}")
    print(f"Request Body (JSON): {request.json}")
    print(f"Request Body (Form Data): {request.form}")

    # --- Placeholder: Extract Message Data ---
    user_id = "test_user_123"
    message_text = "Hey Fylgja. Today I finished the presentation!"

    print(f"Extracted User ID: {user_id}")
    print(f"Extracted Message Text: '{message_text}'")

    # 2. Store the raw incoming message in Firestore (Fylgja's Memory)
    try:
        incoming_message_data = {
            "userId": user_id,
            "timestamp": SERVER_TIMESTAMP,  # <-- Fixed: use imported SERVER_TIMESTAMP
            "rawRequest": {
                "method": request.method,
                "headers": dict(request.headers),
                "jsonBody": request.json,
                "formBody": dict(request.form),
            },
        }
        # Add a new document to the 'incomingMessages' collection
        doc_ref = db.collection("incomingMessages").add(incoming_message_data)
        print(f"Successfully logged message to Firestore. Document ID: {doc_ref[1].id}")

    except Exception as e:
        print(f"Error logging message to Firestore: {e}")
        return Response(f"Error processing message: {e}", status=500)

    # 3. Respond to the messaging platform
    response_message = {
        "status": "success",
        "received": True,
        "message": "Message received by Fylgja!",
    }
    return Response(str(response_message), status=200, mimetype="application/json")


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def local_entrypoint():
    return receive_fylgja_message(request)


if __name__ == "__main__":
    # For local development/testing only; use waitress-serve for production
    app.run(host="127.0.0.1", port=8081, debug=False)
