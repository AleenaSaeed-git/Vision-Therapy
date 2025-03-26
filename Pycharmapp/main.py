
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import json
import os
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
import firebase_admin
from firebase_admin import credentials, firestore
import requests



# Check if Firebase app is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("stereogram-eye-exercise-firebase-adminsdk-fbsvc-d418c39993.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

Builder.load_string("""
#:import get_color_from_hex kivy.utils.get_color_from_hex
""")


class MainScreen(Screen):
    pass

class ExerciseScreen(Screen):
    pass

class LabelButton(ButtonBehavior, Label):
    pass

class LoginScreen(Screen):
    def sign_up(self, email, password):
        app = App.get_running_app()
        email = email.strip()
        password = password.strip()

        if not email or not password:
            self.ids.login_message.text = "Enter Email and Password"
            return

        # Simulate login or signup process
        print(f"Signing up with {email}")

class SettingsScreen(Screen):
    pass



class CalendarScreen(Screen):
    pass


class NotificationScreen(Screen):
    pass

# --- Constants ---
RECORD_FILE = "exercise_records.json"
TOKEN_FILE = "user_token.json"  # File to store authentication token
DEFAULT_EXERCISE_DURATION = 3  # 3 minutes



# Load & Save Exercise Records
def load_records():
    try:
        if os.path.exists(RECORD_FILE):
            with open(RECORD_FILE, "r") as file:
                return json.load(file)
    except json.JSONDecodeError:
        print("⚠ Error reading exercise records. Resetting file.")
        return {"completed_days": [], "exercise_duration": DEFAULT_EXERCISE_DURATION}
    return {"completed_days": [], "exercise_duration": DEFAULT_EXERCISE_DURATION}


def save_records(records):
    try:
        with open(RECORD_FILE, "w") as file:
            json.dump(records, file)
    except Exception as e:
        print(f"⚠ Error saving exercise records: {e}")


# --- Load & Save Authentication Token ---
def save_token(data):
    """Save user authentication token."""
    try:
        with open(TOKEN_FILE, "w") as file:
            json.dump(data, file)
    except Exception as e:
        print(f"⚠ Error saving authentication token: {e}")




FIREBASE_API_KEY = "AIzaSyDd7PwMeucWYmA1yJRUI07ulLiemZuV-L8"
def load_token():
    """✅ Load user token and check if it is valid."""
    try:
        with open("user_session.json", "r") as f:
            token_data = json.load(f)

        id_token = token_data.get("id_token")
        refresh_token = token_data.get("refresh_token")

        if not id_token or not refresh_token:
            print("❌ No valid token found.")
            return None

        if is_token_expired(id_token):
            print("🔄 Token expired! Refreshing...")
            token_data = refresh_id_token(refresh_token)
            if token_data:
                return token_data  # ✅ Return updated token
            return None  # Refresh failed

        return token_data  # ✅ Token is valid
    except Exception as e:
        print("❌ Error loading token:", e)
        return None


import jwt

def is_token_expired(id_token):
    """ Check if Firebase ID token is expired."""
    try:
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        exp_time = decoded_token.get("exp")

        if exp_time:
            import time
            return exp_time < time.time()  # Check if token is expired
        return True  # Default to expired if no expiration found
    except Exception as e:
        print("❌ Error decoding token:", e)
        return True  # Assume expired if there's an error

def refresh_id_token(refresh_token):
    """✅ Refresh expired Firebase token using the refresh token."""
    refresh_url = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_API_KEY}"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    try:
        response = requests.post(refresh_url, data=payload)
        data = response.json()

        if "id_token" in data:
            # ✅ Save new token
            new_token_data = {
                "id_token": data["id_token"],
                "refresh_token": data["refresh_token"],
                "local_id": data["user_id"]
            }

            with open("user_session.json", "w") as f:
                json.dump(new_token_data, f)

            return new_token_data  # ✅ Return new token
        else:
            print("❌ Failed to refresh token:", data)
            return None
    except Exception as e:
        print("❌ Error refreshing token:", e)
        return None

def load_user_id():
    """✅ Fetch the logged-in user ID from session."""
    session_file = "user_session.json"
    if os.path.exists(session_file):
        with open(session_file, "r") as f:
            auth_data = json.load(f)
            return auth_data.get("local_id", "UnknownUser")  # ✅ Prevent None errors
    return "UnknownUser"

def clear_token():
    """Logout by deleting stored token."""
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)


def format_time(seconds):
    minutes = seconds // 60
    seconds %= 60
    return f"{minutes:02}:{seconds:02}"


class NotificationScreen:
    pass


class VisionTherapyApp(App):
    refresh_token_file = "refresh_token.json"

    def build(self):

        Builder.load_file("loginscreen.kv")
        Builder.load_file("calendarscreen.kv")
        Builder.load_file("settingsscreen.kv")
        Builder.load_file("notification_screen.kv")
        Builder.load_file("exercise_screen.kv")

        from loginscreen import LoginScreen
        from calendarscreen import CalendarScreen
        from settingsscreen import SettingsScreen
        from notificationscreen import NotificationScreen
        from mainscreen import MainScreen
        import exercisescreen

        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name="login"))  # Add Login Screen
        self.sm.add_widget(MainScreen(name="main_screen"))
        self.sm.add_widget(exercisescreen.StereogramScreen(name="exercise_screen"))
        self.sm.add_widget(exercisescreen.PencilPushUpScreen(name="pencil_screen"))
        self.sm.add_widget(SettingsScreen(name="settings_screen"))
        self.sm.add_widget(NotificationScreen(name="notification_screen"))
        self.sm.add_widget(CalendarScreen(name="calendar_screen"))

        # --- Auto-login ---
        token_data = load_token()
        if token_data:
            print("✅ Auto-login successful!")
            self.sm.current = "main_screen"  # Skip login if token is valid
        else:
            print("🔑 No valid session found, redirecting to login.")
            self.sm.current = "login_screen"  # Force login if token is missing/expired


        return self.sm

    def change_screen(self, screen_name, direction="left", mode="push"):
        """✅ Switch screens in ScreenManager"""
        if hasattr(self, "sm"):  # ✅ Check if `self.sm` exists before using it
            self.sm.transition.direction = direction
            self.sm.transition.mode = mode
            self.sm.current = screen_name
        else:
            print("❌ Error: ScreenManager (`self.sm`) is not initialized!")

if __name__ == "__main__":
    VisionTherapyApp().run()
