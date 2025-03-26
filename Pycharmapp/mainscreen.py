
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from main import load_records, clear_token
Builder.load_file("kv/MainScreen.kv")

# --- Main Screen ---

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def switch_screen(self, screen_name, instance):
        """Handle logout and switch screens."""
        print(f"Switching to {screen_name}")
        if screen_name == "login_screen":
            clear_token()  # Logout user
        self.manager.current = screen_name
