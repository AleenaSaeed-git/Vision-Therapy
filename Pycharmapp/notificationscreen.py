from plyer import notification
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import threading
import time
from kivy.uix.textinput import TextInput
import requests
import json

FCM_SERVER_KEY = "YOUR_FCM_SERVER_KEY_HERE"
FCM_URL = "https://fcm.googleapis.com/fcm/send"

class NotificationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Schedule notifications every hour (3600 seconds)
        Clock.schedule_interval(lambda dt: self.show_local_notification(), 3600)

    def set_fcm_reminder(self):
        """✅ Send Firebase Cloud Messaging (FCM) reminder"""
        reminder_time = self.ids.reminder_time.text.strip()

        if not reminder_time:
            print("⚠️ Please enter a valid time (HH:MM)")
            return

        try:
            hour, minute = map(int, reminder_time.split(":"))
        except ValueError:
            print("⚠️ Invalid time format! Use HH:MM (24-hour format).")
            return

        # ✅ Prepare the notification payload
        payload = {
            "to": "/topics/reminders",  # Subscribe users to "reminders" topic
            "notification": {
                "title": "Vision Therapy Reminder",
                "body": f"Time for your exercise at {reminder_time}!",
                "sound": "default"
            },
            "data": {
                "reminder_time": reminder_time
            }
        }

        headers = {
            "Authorization": f"key={FCM_SERVER_KEY}",
            "Content-Type": "application/json"
        }

        # ✅ Send the notification
        response = requests.post(FCM_URL, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print(f"✅ Reminder set for {reminder_time} successfully!")
        else:
            print(f"❌ Failed to send reminder! {response.text}")


    def show_local_notification(self):
        """✅ Display a local notification"""
        notification.notify(
            title="Vision Therapy Reminder",
            message="It's time for your exercise!",
            timeout=10
        )

    # ✅ Run background notification service using threading
    @staticmethod
    def background_notification_service():
        while True:
            notification.notify(
                title="Vision Therapy Reminder",
                message="It's time for your exercise!",
                timeout=10
            )
            time.sleep(60 * 60)  # ✅ Wait for 1 hour before next notification

    # Start the background thread
    threading.Thread(target=background_notification_service, daemon=True).start()






