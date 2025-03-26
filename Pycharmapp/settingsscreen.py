import re
from kivy.uix.screenmanager import Screen
from main import load_records, save_records
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from firebase_admin import firestore
from kivy.app import App
from main import load_user_id

db = firestore.client()  # Firestore instance

# --- Settings Screen ---
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.user_id = load_user_id() or "UnknownUser"
        if not self.user_id:
            print("❌ Error: No user logged in.")
        # Replace with actual user ID
        self.load_exercise_duration()  # ✅ Load user settings from Firebase

    def show_timer_popup(self):
        """Show pop-up for setting exercise duration."""
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.timer_input = TextInput(hint_text="Enter duration (minutes)", multiline=False)
        save_button = Button(text="Save", size_hint_y=None, height=50)
        save_button.bind(on_release=self.save_timer_duration)  # ✅ Fix method reference

        layout.add_widget(self.timer_input)
        layout.add_widget(save_button)

        self.popup = Popup(title="Set Exercise Duration", content=layout, size_hint=(0.8, 0.4))
        self.popup.open()

    def save_timer_duration(self, instance):
        """✅ Save entered exercise duration in Firebase & update UI."""
        exercise_time = self.timer_input.text.strip()

        if exercise_time.isdigit():
            exercise_time = int(exercise_time)

            # ✅ Save to Firebase
            db.collection("users").document(self.user_id).set({"exercise_duration": exercise_time}, merge=True)

            # ✅ Update UI
            if "current_timer" in self.ids:
                self.ids.current_timer.text = f"Current Duration: {exercise_time} min"
            else:
                print(f"✅ Exercise duration set to {exercise_time} minutes.")  # Debugging log

            # ✅ Update Exercise Screen timer
            app = App.get_running_app()
            exercise_screen = app.root.get_screen("exercise_screen")
            if hasattr(exercise_screen, "update_exercise_duration"):
                exercise_screen.update_exercise_duration(exercise_time)
            else:
                print("❌ Error: `update_exercise_duration()` not found in ExerciseScreen.")

            self.popup.dismiss()
        else:
            self.timer_input.text = ""
            self.timer_input.hint_text = "Enter a number only !"

    def apply_new_duration(self, new_duration_seconds):
        """🔄 Update exercise duration in all exercise screens immediately."""
        exercise_screen = self.manager.get_screen("pencil_screen")  # Fetch Pencil Push-Up Screen
        stereogram_screen = self.manager.get_screen("exercise_screen")  # Fetch Stereogram Screen

        # ✅ Apply new duration
        exercise_screen.update_exercise_duration(new_duration_seconds)
        stereogram_screen.update_exercise_duration(new_duration_seconds)

        print(f"🔄 Updated exercise screens to {new_duration_seconds} seconds.")

    def load_exercise_duration(self):
        """✅ Load exercise duration from Firebase and convert to minutes"""
        user_id = load_user_id()
        if not user_id:
            print("❌ No user logged in.")
            return

        from main import db
        doc_ref = db.collection("users").document(user_id)
        doc = doc_ref.get()

        if doc.exists:
            saved_duration = doc.to_dict().get("exercise_duration", 180)  # Default 180 seconds (3 min)

            # ✅ Convert seconds to minutes before displaying
            self.ids.exercise_duration_input.text = str(saved_duration // 60)
            self.ids.current_timer.text = f"Current Duration: {saved_duration // 60} min"

            print(f"✅ Loaded exercise duration: {saved_duration // 60} minutes")
        else:
            print("⚠ No exercise duration found in Firebase.")


