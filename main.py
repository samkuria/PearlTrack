# main.py
from firebase_realtime import initialize_firebase
from dashboard import launch_dashboard

# Initialize Firebase only once
initialize_firebase()


if __name__ == "__main__":
    launch_dashboard()


