# Vision Therapy Application

A Kivy-based application for vision therapy exercises, featuring Firebase integration for user management and notifications.

## Features

- User Authentication
- Two types of eye exercises:
  - Stereogram exercises
  - Pencil Push-up exercises
- Exercise Timer with Progress Tracking
- Calendar View for Exercise History
- Customizable Exercise Duration
- Push Notifications for Exercise Reminders
- Firebase Integration for Data Storage

## Quick Start Guide

1. Clone the repository:
```bash
git clone https://github.com/AleenaSaeed-git/Vision-Therapy.git
cd Vision-Therapy
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

## Important Files and Their Purposes

1. `firebase_service_key.json`:
   - Contains Firebase service account credentials
   - Required for Firebase authentication and database access
   - Already included in the repository for easy setup

2. `user_session.json`:
   - Stores user login information
   - Created automatically when you first log in
   - Contains your FCM token for notifications

3. `exercise_progress.json`:
   - Saves your exercise progress locally
   - Created automatically when you start exercises
   - Helps resume exercises if the app is closed

4. `refresh_token.json`:
   - Stores Firebase authentication refresh token
   - Created automatically during login
   - Helps maintain your login session

## Firebase Configuration

The application is pre-configured with Firebase settings. The following files contain the necessary configuration:

1. `firebase_service_key.json`:
   - Contains the service account credentials
   - Already included in the repository
   - No changes needed

2. Firebase API Key in `main.py`:
   - Pre-configured with the project API key
   - No changes needed

## Common Issues and Solutions

1. "Firebase Authentication Error":
   - Make sure you have an active internet connection
   - Try logging out and logging back in
   - Check if the Firebase service is running

2. "Notification Not Working":
   - Check if notifications are enabled in your system settings
   - Try setting a new reminder time
   - Make sure the app is running in the background

3. "Exercise Timer Not Working":
   - Check if the app has focus
   - Try restarting the exercise
   - Make sure your system time is correct

## Project Structure

```
Vision-Therapy/
├── main.py                 # Main application entry point
├── exercisescreen.py       # Exercise screen implementation
├── notificationscreen.py   # Notification management
├── fcm_utils.py           # Firebase Cloud Messaging utilities
├── fcm_client.py          # FCM client implementation
├── fcm_token_manager.py   # FCM token management
├── auth_utils.py          # Authentication utilities
├── requirements.txt       # Project dependencies
├── firebase_service_key.json  # Firebase service account key
└── .gitignore            # Git ignore rules
```

## Usage Guide

1. First Time Setup:
   - Run the application using `python main.py`
   - Create a new account or log in
   - The app will automatically set up all necessary files

2. Exercise Sessions:
   - Choose between Stereogram or Pencil Push-up exercises
   - Set your preferred duration in Settings
   - Follow on-screen instructions
   - Track your progress in the Calendar view

3. Notifications:
   - Go to Settings → Customize Notification Time
   - Enter your preferred reminder time (HH:MM format)
   - Save the settings
   - You'll receive notifications at the specified time

## Support

For support or questions:
1. Check the Common Issues section above
2. Make sure all required files are present
3. Verify your internet connection
4. Contact the maintainers if issues persist

## Note

This repository contains all necessary configuration files for immediate use. No additional setup is required beyond installing the dependencies and running the application. 