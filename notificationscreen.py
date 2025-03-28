from plyer import notification
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import threading
import time
from kivy.uix.textinput import TextInput
import requests
import json
from fcm_utils import send_fcm_notification
from fcm_token_manager import get_fcm_token, initialize_fcm_token

class NotificationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notification_thread = None
        self.is_notification_active = False

    def set_fcm_reminder(self):
        """Send Firebase Cloud Messaging (FCM) reminder"""
        reminder_time = self.ids.reminder_time.text.strip()

        if not reminder_time:
            print("⚠️ Please enter a valid time (HH:MM)")
            return

        try:
            hour, minute = map(int, reminder_time.split(":"))
        except ValueError:
            print("⚠️ Invalid time format! Use HH:MM (24-hour format).")
            return

        # Get the FCM token
        fcm_token = get_fcm_token()
        if not fcm_token:
            print("⚠️ FCM token not found. Attempting to initialize...")
            if not initialize_fcm_token():
                print("❌ Failed to initialize FCM token")
                return
            fcm_token = get_fcm_token()

        if not fcm_token:
            print("❌ Error: FCM token not found")
            return

        # Send the notification
        try:
            send_fcm_notification(
                token=fcm_token,
                title="Vision Therapy Reminder",
                body=f"Time for your exercise at {reminder_time}!"
            )
            print(f"✅ Reminder set for {reminder_time} successfully!")
        except Exception as e:
            print(f"❌ Failed to send reminder! {str(e)}")

    def show_local_notification(self):
        """Display a local notification"""
        try:
            notification.notify(
                title="Vision Therapy Reminder",
                message="It's time for your exercise!",
                timeout=10
            )
        except Exception as e:
            print(f"❌ Failed to show local notification: {str(e)}")

    def start_notification_service(self):
        """Start the background notification service"""
        if not self.is_notification_active:
            self.is_notification_active = True
            self.notification_thread = threading.Thread(
                target=self._notification_service,
                daemon=True
            )
            self.notification_thread.start()
            print("✅ Notification service started")

    def stop_notification_service(self):
        """Stop the background notification service"""
        self.is_notification_active = False
        if self.notification_thread:
            self.notification_thread.join(timeout=1)
            print("✅ Notification service stopped")

    def _notification_service(self):
        """Background notification service implementation"""
        while self.is_notification_active:
            self.show_local_notification()
            time.sleep(3600)  # Wait for 1 hour before next notification

    def on_leave(self):
        """Clean up when leaving the screen"""
        self.stop_notification_service()






