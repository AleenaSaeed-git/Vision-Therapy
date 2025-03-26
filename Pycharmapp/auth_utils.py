import json

def get_logged_in_user(self):
    """Retrieve logged-in user's details from file"""
    try:
        with open("refresh_token.json", "r") as f:  # Replace with your stored file
            auth_data = json.load(f)
            return auth_data.get("local_id"), auth_data.get("email")
    except FileNotFoundError:
        return None, None

import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_service_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_fcm_token(user_id, token):
    """Save or update user's FCM token in Firestore"""
    user_ref = db.collection("users").document(user_id)
    user_ref.set({"fcm_token": token}, merge=True)
    print(f"✅ FCM Token saved for {user_id}")
