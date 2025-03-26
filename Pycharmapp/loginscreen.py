from kivy.uix.screenmanager import Screen
import requests
import json
import os
from kivy.app import App
from kivy.utils import get_color_from_hex
from auth_utils import get_logged_in_user


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.auto_login()  # ✅ Auto-login on app start

    wak = "AIzaSyDd7PwMeucWYmA1yJRUI07ulLiemZuV-L8"

    def sign_up(self, email, password):
        app = App.get_running_app()
        if not app:
            print("App is not running yet!")
            return

        email = email.strip()
        password = password.strip()
        if not email or not password:
            self.ids.login_message.text = "Enter Email and Password"
            return

        signup_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.wak}"
        signup_payload = {"email": email, "password": password, "returnSecureToken": True}

        response = requests.post(signup_url, json=signup_payload)
        sign_up_data = response.json()

        if response.ok:
            auth_data = {
                "refresh_token": sign_up_data["refreshToken"],
                "local_id": sign_up_data["localId"],
                "id_token": sign_up_data["idToken"],
                "email": email
            }

            self.save_login_session(auth_data)  # ✅ Save session data

            app.local_id = sign_up_data["localId"]
            app.id_token = sign_up_data["idToken"]
            app.user_email = email
            self.ids.login_message.text = "Signup Successful! You can log in."

        else:
            error_message = sign_up_data.get("error", {}).get("message", "Unknown Error")
            if error_message == "EMAIL_EXISTS":
                self.sign_in_existing_user(email, password)
            else:
                self.ids.login_message.text = error_message.replace("_", " ")

    def save_login_session(self, auth_data):
        """✅ Save user session locally"""
        with open("user_session.json", "w") as f:
            json.dump(auth_data, f)

    def sign_in_existing_user(self, email, password):
        """Sign in if the user already exists"""
        app = App.get_running_app()
        email = email.strip()
        password = password.strip()

        if not email or not password:
            self.ids.login_message.text = "Enter Email and Password"
            return

        login_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.wak}"
        login_payload = {"email": email, "password": password, "returnSecureToken": True}

        try:
            response = requests.post(login_url, json=login_payload)
            login_data = response.json()

            if response.ok:
                auth_data = {
                    "refresh_token": login_data["refreshToken"],
                    "local_id": login_data["localId"],
                    "id_token": login_data["idToken"],
                    "email": email
                }

                self.save_login_session(auth_data)  # ✅ Save login session

                # Store values in the app instance
                app.local_id = login_data["localId"]
                app.id_token = login_data["idToken"]
                app.user_email = email  # ✅ Store user email
                app.root.current = "main_screen"  # ✅ Navigate to the main screen

            else:
                error_message = login_data.get("error", {}).get("message", "Unknown Error")
                self.ids.login_message.text = error_message.replace("_", " ")

        except Exception as e:
            self.ids.login_message.text = "Login failed. Check internet connection."
            print(f"Error during login: {e}")

    def auto_login(self):
        """✅ Check if user session exists and log in automatically"""
        try:
            if os.path.exists("user_session.json"):
                with open("user_session.json", "r") as f:
                    auth_data = json.load(f)

                id_token, user_id = self.exchange_refresh_token(auth_data["refresh_token"])
                if id_token:
                    app = App.get_running_app()
                    app.local_id = user_id
                    app.id_token = id_token
                    app.user_email = auth_data["email"]  # ✅ Restore email
                    app.root.current = "main_screen"
        except Exception as e:
            print("Auto-login failed:", e)

    def exchange_refresh_token(self, refresh_token):
        """✅ Get a new ID token using a refresh token"""
        refresh_url = f"https://securetoken.googleapis.com/v1/token?key={self.wak}"
        refresh_payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        refresh_req = requests.post(refresh_url, json=refresh_payload)
        refresh_data = refresh_req.json()

        if refresh_req.ok:
            new_id_token = refresh_data["id_token"]
            user_id = refresh_data["user_id"]

            # ✅ Update session with new ID token
            with open("user_session.json", "r+") as f:
                auth_data = json.load(f)
                auth_data["id_token"] = new_id_token
                f.seek(0)
                json.dump(auth_data, f)
                f.truncate()

            return new_id_token, user_id
        else:
            print("Failed to refresh token:", refresh_data)
            return None, None

    def logout(self):
        """✅ Log out the user and clear session data"""
        if os.path.exists("user_session.json"):
            os.remove("user_session.json")  # ✅ Delete session file

        # ✅ Reset app variables
        app = App.get_running_app()
        app.local_id = None
        app.id_token = None
        app.user_email = None

        self.manager.current = "login_screen"


