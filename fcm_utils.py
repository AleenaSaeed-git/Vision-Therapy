import requests
import json
import os

def load_firebase_key():
    """Load Firebase service key from file"""
    try:
        with open("firebase_service_key.json", "r") as f:
            service_data = json.load(f)
            if "private_key" not in service_data:
                raise KeyError("❌ 'private_key' not found in firebase_service_key.json")
            return service_data["private_key"]
    except FileNotFoundError:
        raise FileNotFoundError("❌ firebase_service_key.json not found")
    except json.JSONDecodeError:
        raise ValueError("❌ Invalid JSON in firebase_service_key.json")

# Load Firebase Server Key
try:
    SERVER_KEY = load_firebase_key()
except Exception as e:
    print(f"❌ Error loading Firebase key: {str(e)}")
    SERVER_KEY = None

FIREBASE_API_URL = "https://fcm.googleapis.com/fcm/send"

def send_fcm_notification(token, title, body):
    """Send an FCM push notification"""
    if not SERVER_KEY:
        raise ValueError("❌ Firebase server key not loaded")

    # Check if this is a test token
    if token.startswith("test_token_"):
        print("⚠️ Using test token - notification will be simulated")
        print(f"📱 Would send notification to {token}")
        print(f"📝 Title: {title}")
        print(f"📝 Body: {body}")
        return True

    headers = {
        "Authorization": f"key={SERVER_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "to": token,
        "notification": {
            "title": title,
            "body": body,
            "sound": "default"
        },
        "priority": "high"
    }
    
    try:
        response = requests.post(FIREBASE_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        result = response.json()
        
        if "message_id" in result:
            print("✅ FCM notification sent successfully")
            return True
        else:
            print(f"❌ FCM notification failed: {result}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending FCM notification: {str(e)}")
        raise
