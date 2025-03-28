import json
import os
import requests
from auth_utils import save_fcm_token
from fcm_client import initialize_fcm, get_fcm_client

def initialize_fcm_token():
    """Initialize FCM token and save it to user session and Firebase"""
    try:
        # Initialize FCM client
        if not initialize_fcm():
            print("❌ Failed to initialize FCM")
            return False

        # Get FCM client instance
        fcm_client = get_fcm_client()
        
        # Load user session
        with open("user_session.json", "r") as f:
            user_data = json.load(f)
            user_id = user_data.get("local_id")
            
        if user_id:
            # Save token to Firebase and user session
            if fcm_client.save_token(user_id):
                print("✅ FCM token initialized and saved successfully")
                return True
            else:
                print("❌ Failed to save FCM token")
                return False
        else:
            print("❌ No user ID found in session")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing FCM token: {str(e)}")
        return False

def get_fcm_token():
    """Get FCM token from user session"""
    try:
        with open("user_session.json", "r") as f:
            user_data = json.load(f)
            return user_data.get("fcm_token")
    except (FileNotFoundError, json.JSONDecodeError):
        return None 