from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from datetime import datetime, timedelta
from kivy.properties import StringProperty
import firebase_admin
from firebase_admin import credentials, firestore
from kivy.clock import Clock
from firebase_admin import auth
import json
from auth_utils import get_logged_in_user
from datetime import datetime
from fcm_utils import send_fcm_notification
from main import load_user_id

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("stereogram-eye-exercise-firebase-adminsdk-fbsvc-d418c39993.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- CalendarScreen ---

class CalendarScreen(Screen):
    current_month = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.today = datetime.today()
        self.current_date = self.today.replace(day=1)  # ✅ Always start at the 1st of the month
        self.completed_days = []  # ✅ Store fetched completed days
        self.user_id = load_user_id()
        if not self.user_id:
            print("❌ Error: No user logged in.")

        self.user_email = None

        self.update_month_label()
        self.load_user_data()

    def refresh_completed_days(self, completed_day):
        """🔄 Update UI to mark completed days in green"""
        if completed_day not in self.completed_days:
            self.completed_days.append(completed_day)
            self.update_calendar()  # ✅ Refresh UI after updating data

    def update_ui(self):
        """🔄 Redraw the calendar with green marks on completed days"""
        for day in self.ids.calendar_grid.children:
            if day.text in self.completed_days:
                day.background_color = (0, 1, 0, 1)  # ✅ Turn button green

    def update_month_label(self):
        """✅ Update the displayed month"""
        self.current_month = self.current_date.strftime("%B %Y")

    def change_month(self, direction):
        """✅ Change calendar month"""
        new_month = self.current_date.month + direction
        new_year = self.current_date.year

        if new_month > 12:
            new_month = 1
            new_year += 1
        elif new_month < 1:
            new_month = 12
            new_year -= 1

        self.current_date = datetime(new_year, new_month, 1)  # ✅ Fix: Use `datetime()`
        self.update_month_label()
        self.fetch_completed_days()

    def load_user_data(self):
        """✅ Load user session from local storage"""
        try:
            with open("user_session.json", "r") as f:
                auth_data = json.load(f)
                self.user_id = auth_data.get("local_id")
                self.user_email = auth_data.get("email")

                if self.user_id:
                    self.fetch_completed_days()
        except Exception as e:
            print("Error loading user session:", e)

    def fetch_completed_days(self):
        """✅ Fetch completed exercise days from Firestore"""
        if not self.user_id:
            print("No user logged in")
            return

        doc_ref = db.collection("users").document(self.user_id)
        doc = doc_ref.get()

        if doc.exists:
            completed_raw = doc.to_dict().get("completed_days", [])
            self.completed_days = [day.strip() for day in completed_raw]  # ✅ Normalize format
            print(f"✅ Completed Days (from Firestore): {self.completed_days}")

        else:
            self.completed_days = []

        self.update_calendar()  # ✅ Refresh calendar with fetched data

    def set_fcm_reminder(self):
        """Save reminder time and schedule FCM notification"""
        user_id = self.user_id
        reminder_time = self.ids.reminder_time.text.strip()

        if not reminder_time:
            print("❌ Reminder time not set")
            return

        user_ref = db.collection("users").document(user_id)

        # 🔹 Ensure the token is stored correctly
        doc = user_ref.get()
        if doc.exists:
            fcm_token = doc.to_dict().get("fcm_token", "")
            if not fcm_token:
                print("⚠ No FCM token found! Make sure user has granted notifications.")
                return  # ✅ Prevent sending empty notifications
        else:
            print("❌ User document does not exist!")
            return

        # ✅ Save reminder in Firestore
        user_ref.set({"reminder_time": reminder_time}, merge=True)

        # ✅ Send FCM Notification
        send_fcm_notification(fcm_token, "Exercise Reminder", f"Time to do your exercise at {reminder_time}!")

        print(f"✅ Reminder set for {reminder_time}")

    def update_calendar(self, dt=None):
        """✅ Populate the calendar with Firestore data"""
        if not hasattr(self.ids, "calendar_grid"):
            print("❌ Error: 'calendar_grid' not found in UI")
            return

        self.ids.calendar_grid.clear_widgets()

        first_day = self.current_date.replace(day=1)
        last_day = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)).day

        for _ in range(first_day.weekday()):  # Empty slots before 1st
            self.ids.calendar_grid.add_widget(Label(text=""))

        for day in range(1, last_day + 1):
            date_str = first_day.strftime("%Y-%m") + f"-{day:02}"
            btn = Button(text=str(day), size_hint=(1, 1))
            btn.background_normal = ""  # ✅ Ensure color change

            if date_str in self.completed_days:
                btn.background_color = (0, 1, 0, 1)  # ✅ Green for completed days
                btn.color = (1, 1, 1, 1)  # ✅ White text
            elif datetime.strptime(date_str, "%Y-%m-%d") < datetime.today():
                btn.background_color = (1, 0, 0, 1)  # ✅ Red for missed days
                btn.color = (1, 1, 1, 1)  # ✅ White text
            else:
                btn.background_color = (1, 1, 1, 1)  # ✅ White for upcoming days
                btn.color = (0, 0, 0, 1)  # ✅ Black text

            self.ids.calendar_grid.add_widget(btn)



    def update_calendar_ui(self, completed_day):
        """🔄 Refresh calendar after exercise completion"""
        calendar_screen = self.manager.get_screen("calendar_screen")  # ✅ Get Calendar Screen

        # ✅ Ensure 'calendar_screen' has a method to update UI
        if hasattr(calendar_screen, "refresh_completed_days"):
            calendar_screen.refresh_completed_days(completed_day)
        else:
            print("⚠ Calendar UI update method not found!")