import requests
import json

# 🔹 Load Firebase Server Key
with open("firebase_service_key.json", "r") as f:
    service_data = json.load(f)
# 🔹 Ensure 'private_key' exists
if "private_key" in service_data:
    SERVER_KEY = service_data["private_key"]
else:
    raise KeyError("❌ 'private_key' not found in firebase_service_key.json")

FIREBASE_API_URL = "https://fcm.googleapis.com/fcm/send"

def send_fcm_notification(token, title, body):
    """Send an FCM push notification"""
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
    response = requests.post(FIREBASE_API_URL, headers=headers, json=data)
    print("FCM Response:", response.json())
