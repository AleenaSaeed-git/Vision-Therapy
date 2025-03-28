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

## Prerequisites

- Python 3.8 or higher
- Firebase project with Cloud Messaging enabled
- Firebase service account key

## Installation

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

4. Set up Firebase:
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Enable Authentication and Cloud Firestore
   - Download your service account key and save it as `firebase_service_key.json` in the project root

## Configuration

1. Firebase Setup:
   - Place your `firebase_service_key.json` in the project root
   - The file should contain your Firebase service account credentials

2. Notification Settings:
   - Go to Settings → Customize Notification Time
   - Enter your preferred reminder time in HH:MM format (24-hour)

## Usage

1. Start the application:
```bash
python main.py
```

2. User Registration/Login:
   - Create a new account or log in with existing credentials
   - Your progress will be saved to Firebase

3. Exercise Sessions:
   - Choose between Stereogram or Pencil Push-up exercises
   - Set your preferred duration in Settings
   - Follow on-screen instructions
   - Track your progress in the Calendar view

4. Notifications:
   - Set up exercise reminders in the Notification settings
   - Receive push notifications at your specified time

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
└── .gitignore            # Git ignore rules
```

## Firebase Integration

The application uses Firebase for:
- User Authentication
- Data Storage (exercise history, settings)
- Push Notifications

Make sure to:
1. Enable Email/Password authentication in Firebase Console
2. Set up Cloud Firestore database
3. Configure Cloud Messaging for notifications

## Troubleshooting

1. Firebase Connection Issues:
   - Verify your `firebase_service_key.json` is present and valid
   - Check your internet connection
   - Ensure Firebase services are enabled in your project

2. Notification Problems:
   - Check notification permissions
   - Verify FCM token is properly saved
   - Ensure correct time format in settings

3. Exercise Timer Issues:
   - Check if exercise duration is set correctly
   - Verify Firebase connection for saving progress

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 