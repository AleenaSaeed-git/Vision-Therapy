import json
import os
import time
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.uix.progressbar import ProgressBar
from kivy.animation import Animation
from datetime import datetime, timedelta
from kivy.properties import StringProperty
from firebase_admin import firestore
from main import load_user_id

# --- ExerciseScreen ---
class ExerciseScreen(Screen):
    """Base class for exercise screens (Stereogram & Pencil Push-Up)"""

    def __init__(self, exercise_type, exercise_image, instruction_image, **kwargs):
        super().__init__(**kwargs)
        self.exercise_type = exercise_type
        self.exercise_image = exercise_image
        self.instruction_image = instruction_image
        self.db = firestore.client()
        self.user_id = load_user_id()
        if not self.user_id:
            print("❌ Error: No user logged in.")

        self.exercise_duration = 180  # Default to 3 minutes
        self.remaining_time = self.exercise_duration  # ✅ Initialize remaining time
        self.paused = False  # Flag to track if paused

        # --- Load Notification Sound ---
        self.alert_sound = SoundLoader.load("alert_sound.mp3")  # Ensure this file is in your project folder
        Clock.schedule_once(self.initialize_ui, 0.1)

    def initialize_ui(self, dt):
        """Make sure UI elements are loaded before using them"""
        self.timer_label = self.ids.timer_label
        self.progress_bar = self.ids.progress_bar
        self.start_button = self.ids.start_button

        self.load_timer_progress()  # ✅ Load previous progress

        self.progress_bar.max = self.exercise_duration
        self.progress_bar.value = self.remaining_time

    def start_exercise(self, *args):
        """Start, pause, and resume the timer with progress animation"""
        if self.remaining_time <= 0:  # Restart if finished
            self.remaining_time = self.exercise_duration
            self.progress_bar.value = self.exercise_duration

        if not self.paused:
            Clock.schedule_interval(self.update_timer, 1)  # ✅ Start timer
            self.start_button.text = "Pause"
        else:
            Clock.unschedule(self.update_timer)  # ✅ Pause timer
            self.start_button.text = "Resume"

        self.paused = not self.paused  # Toggle pause state


    def update_timer(self, dt):
        """Update countdown timer, progress bar, and play sound when time's up."""
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.text = f"Time: {self.remaining_time // 60}:{self.remaining_time % 60:02d}"

            # ✅ Smooth progress bar animation
            Animation(value=self.remaining_time, duration=0.5).start(self.progress_bar)
        else:
            Clock.unschedule(self.update_timer)  # ✅ Stop timer
            self.timer_label.text = "Time's up!"
            self.start_button.text = "Start Timer"
            self.paused = False  # Reset pause state
            self.mark_exercise_completed()

            if self.alert_sound:
                self.alert_sound.play()  # ✅ Play sound when finished

    def load_exercise_duration(self):
        """🔄 Load updated exercise duration from Firebase"""
        doc_ref = self.db.collection("users").document(self.user_id)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            self.exercise_duration = data.get("exercise_duration", 180)  # Default 3 minutes (180 sec)
            print(f"✅ Loaded exercise duration: {self.exercise_duration // 60} min")
        else:
            self.db.collection("users").document(self.user_id).set({"exercise_duration": 180})

        self.remaining_time = self.exercise_duration
        self.progress_bar.max = self.exercise_duration
        self.progress_bar.value = self.exercise_duration

    def update_exercise_duration(self, new_duration):
        """✅ Update exercise duration in Firebase and refresh UI."""
        user_id = load_user_id()
        if not user_id:
            print("❌ No user logged in.")
            return
        from main import db

        doc_ref = db.collection("users").document(user_id)
        new_duration_seconds = int(new_duration) * 60  # Convert minutes → seconds
        doc_ref.set({"exercise_duration": new_duration_seconds}, merge=True)

        # ✅ Update UI Label
        self.ids.timer_label.text = f"Exercise Duration: {new_duration} min"
        print(f"✅ Exercise duration updated to {new_duration} minutes in Firebase.")

        # 🔄 Apply Changes to Exercise Screens
        self.apply_new_duration(new_duration_seconds)

    def save_timer_progress(self):
        """✅ Save remaining exercise time before closing the app"""
        data = {
            "exercise_type": self.exercise_type,
            "remaining_time": self.remaining_time
        }
        try:
            with open("exercise_progress.json", "w") as file:
                json.dump(data, file)
            print("✅ Timer progress saved.")
        except Exception as e:
            print(f"❌ Error saving timer progress: {e}")

    def mark_exercise_completed(self):
        """✅ Save completed exercises in Firestore & refresh calendar"""
        if not self.user_id:
            print("❌ Error: No user ID found. Please log in.")
            return

        today = datetime.today().strftime("%Y-%m-%d")
        doc_ref = self.db.collection("users").document(self.user_id)
        doc = doc_ref.get()

        # ✅ Get completed days, or initialize empty list
        completed_days = doc.to_dict().get("completed_days", []) if doc.exists else []

        if today not in completed_days:
            completed_days.append(today)
            doc_ref.set({"completed_days": completed_days}, merge=True)  # ✅ Save to Firebase
            print(f"✅ Marked {today} as completed for {self.user_id}")

            # ✅ Ensure calendar updates after completion
            if hasattr(self.manager, "calendar_screen"):
                self.manager.get_screen("calendar_screen").refresh_completed_days(today)

    def load_timer_progress(self):
        """🔄 Load the saved timer progress"""
        if os.path.exists("exercise_progress.json"):
            try:
                with open("exercise_progress.json", "r") as file:
                    data = json.load(file)

                if data.get("exercise_type") == self.exercise_type:
                    self.remaining_time = data.get("remaining_time", self.exercise_duration)
                    print(f"⏳ Loaded saved timer: {self.remaining_time} seconds left")
            except json.JSONDecodeError:
                print("❌ Error reading saved timer data.")

    def load_user_id(self):
        """Fetch logged-in user ID from session."""
        try:
            with open("user_session.json", "r") as f:
                auth_data = json.load(f)
                return auth_data.get("local_id")  # ✅ Get user ID
        except FileNotFoundError:
            print("❌ Error: No user session found.")
            return None  # ✅ No user logged in



    def show_instructions(self, image_path):
        """ Display instructions as a popup instead of switching screens """
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        layout.add_widget(Image(source=image_path))
        close_button = Button(text="Close", size_hint_y=None, height=50)
        layout.add_widget(close_button)

        popup = Popup(title="Exercise Instructions", content=layout, size_hint=(0.8, 0.8))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def on_pre_enter(self):
        """✅ Refresh duration when entering the screen"""
        self.load_exercise_duration()  # 🔄 Fetch updated duration from Firebase
        self.timer_label.text = f"Time: {self.exercise_duration // 60}:{self.exercise_duration % 60:02d}"

    def go_back(self, *args):
        """✅ Save timer before leaving the screen"""
        self.save_timer_progress()
        Clock.unschedule(self.update_timer)  # ✅ Stop timer when exiting
        self.manager.current = "main_screen"


class StereogramScreen(ExerciseScreen):
    exercise_image = StringProperty("stereogram.jpg")

    def __init__(self, **kwargs):
        super().__init__("Stereogram", "stereogram.jpg", "stereogram_instruction.jpeg", **kwargs)
        self.remaining_time = self.exercise_duration

    def update_timer(self, dt):
        """Update the timer and start the progress bar update"""
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.text = f"Time: {self.remaining_time // 60}:{self.remaining_time % 60:02d}"
            self.progress_bar.value = self.remaining_time
        else:
            Clock.unschedule(self.update_timer)
            print("Exercise completed!")
            self.mark_exercise_completed()

    def apply_new_duration(self, new_duration):
        """✅ Apply new exercise duration to the UI"""
        if "timer_label" in self.ids:
            self.ids.timer_label.text = f"Exercise Duration: {new_duration // 60} min"
            print(f"✅ Exercise duration updated to {new_duration // 60} minutes")
        else:
            print("❌ Error: 'timer_label' not found in KV file!")



class PencilPushUpScreen(ExerciseScreen):
    exercise_image = StringProperty("pencil_pushup.jpg")

    def __init__(self, **kwargs):
        super().__init__("Pencil Push-Up", "pencil_pushup.jpg", "pencil_pushup_instruction.jpeg", **kwargs)
        self.remaining_time = self.exercise_duration


    def update_timer(self, dt):
        """Update the timer and start the progress bar update"""
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.text = f"Time: {self.remaining_time // 60}:{self.remaining_time % 60:02d}"
            self.progress_bar.value = self.remaining_time
        else:
            Clock.unschedule(self.update_timer)
            print("Exercise completed!")
            self.mark_exercise_completed()

    def apply_new_duration(self, new_duration):
        """✅ Apply new exercise duration to the UI"""
        if "timer_label" in self.ids:
            self.ids.timer_label.text = f"Exercise Duration: {new_duration // 60} min"
            print(f"✅ Exercise duration updated to {new_duration // 60} minutes")
        else:
            print("❌ Error: 'timer_label' not found in KV file!")
