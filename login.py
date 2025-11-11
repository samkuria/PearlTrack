# login.py
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from utils.device_id import get_device_id
from utils.firebase_service import send_activation_request  # ✅ Firebase integration

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACTIVATION_DB = os.path.join(BASE_DIR, "database", "activation.db")

def is_device_approved():
    """Check if this device is approved to use the software."""
    device_id = get_device_id()
    conn = sqlite3.connect(ACTIVATION_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT approved FROM activations WHERE device_id = ?", (device_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == 1

def save_activation_request(email, device_id):
    """Save an activation request to the DB and send notification to admin (local + Firebase)."""
    conn = sqlite3.connect(ACTIVATION_DB)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO activations (email, device_id) VALUES (?, ?)",
            (email, device_id)
        )
        conn.commit()

        # Optional email notification
        from utils.dev_notify import send_activation_email
        send_activation_email(email, device_id)

        # Backup log
        with open("pending_approvals.txt", "a") as f:
            f.write(f"New activation request:\nEmail: {email}\nDevice ID: {device_id}\n\n")

        # ✅ Send to Firebase
        send_activation_request(device_id, email)

    except sqlite3.IntegrityError:
        pass  # Already requested

    finally:
        conn.close()

def prompt_login():
    """Display login screen for email/password activation request."""
    def on_submit():
        email = entry_email.get()
        password = entry_password.get()

        if not email or not password:
            messagebox.showwarning("Input Error", "Please enter both email and password.")
            return

        device_id = get_device_id()
        save_activation_request(email, device_id)

        messagebox.showinfo("Request Sent", "Your activation request has been sent to the developer.\nPlease wait for approval.")
        root.destroy()

    root = tk.Tk()
    root.title("Software Activation")
    root.geometry("350x160")
    root.resizable(False, False)

    tk.Label(root, text="Email:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_email = tk.Entry(root, width=30)
    entry_password = tk.Entry(root, show="*", width=30)

    entry_email.grid(row=0, column=1, pady=5)
    entry_password.grid(row=1, column=1, pady=5)

    tk.Button(root, text="Submit", command=on_submit, bg="#3498db", fg="white").grid(row=2, column=0, columnspan=2, pady=15)

    root.mainloop()

def login_screen():
    """Entry point for login or activation."""
    if is_device_approved():
        from dashboard import launch_dashboard
        launch_dashboard()
    else:
        prompt_login()




