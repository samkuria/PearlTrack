from datetime import date
from firebase_realtime import initialize_firebase  # Import your Firebase initialization
from firebase_admin import db

# Initialize Firebase (call this once at startup)


def add_appointment(patient_name, contact, reason, appt_date, appt_time):
    """Add a new appointment to Firebase Realtime Database."""
    ref = db.reference('appointments')
    new_appointment = ref.push({
        'patient_name': patient_name,
        'contact': contact,
        'reason': reason,
        'date': appt_date,
        'time': appt_time
    })
    return new_appointment.key  # Returns Firebase-generated ID

def get_todays_appointments():
    """Retrieve today's appointments from Firebase."""
    today = date.today().isoformat()
    ref = db.reference('appointments')
    appointments = ref.order_by_child('date').equal_to(today).get()
    return appointments if appointments else {}

def delete_appointment(appt_id):
    """Delete an appointment from Firebase by its ID."""
    ref = db.reference('appointments')
    ref.child(appt_id).delete()


def get_all_appointments():
    ref = db.reference('appointments')
    appointments = ref.get()  # Retrieve all appointments
    if appointments is None:
        return []  # Return an empty list if there are no appointments
    # Unpack the appointments
    return [
        (id_, appt['patient_name'], appt['contact'], appt['reason'], appt['date'], appt['time'])
        for id_, appt in appointments.items()
    ]








