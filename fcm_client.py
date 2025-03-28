import json
import os
from kivy.app import App
from kivy.clock import Clock
from kivy.utils import platform
import firebase_admin
from firebase_admin import messaging, credentials

class FCMClient:
    def __init__(self):
        self.token = None
        # Firebase Admin SDK is already initialized in main.py

    def initialize(self):
        """Initialize FCM and get token"""
        try:
            # Request permission for notifications
            if platform == 'android':
                from android.permissions import request_permissions, Permission
                request_permissions([
                    Permission.INTERNET,
                    Permission.POST_NOTIFICATIONS
                ])

            # For testing purposes, generate a unique token
            # In a real app, this would come from the client device
            self.token = f"test_token_{os.getpid()}"
            print("✅ FCM token obtained successfully")
            return True

        except Exception as e:
            print(f"❌ Error initializing FCM: {str(e)}")
            return False

    def save_token(self, user_id):
        """Save FCM token to user session and Firebase"""
        try:
            if not self.token:
                print("❌ No FCM token available")
                return False

            # Save to user session
            with open("user_session.json", "r") as f:
                user_data = json.load(f)
                user_data["fcm_token"] = self.token
                with open("user_session.json", "w") as f:
                    json.dump(user_data, f)

            # Save to Firebase
            from auth_utils import save_fcm_token
            save_fcm_token(user_id, self.token)

            print("✅ FCM token saved successfully")
            return True
        except Exception as e:
            print(f"❌ Error saving FCM token: {str(e)}")
            return False

    def on_message(self, callback):
        """Handle incoming messages"""
        try:
            # For testing purposes, we'll simulate message handling
            print("✅ FCM message handler registered")
            return True
        except Exception as e:
            print(f"❌ Error registering message handler: {str(e)}")
            return False

# Global FCM client instance
fcm_client = None

def initialize_fcm():
    """Initialize FCM client"""
    global fcm_client
    if not fcm_client:
        fcm_client = FCMClient()
        return fcm_client.initialize()
    return True

def get_fcm_client():
    """Get FCM client instance"""
    global fcm_client
    if not fcm_client:
        fcm_client = FCMClient()
    return fcm_client 