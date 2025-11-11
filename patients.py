from firebase_realtime import initialize_firebase  # Import your Firebase initialization
from firebase_admin import db

def get_all_patients():
    

    ref = db.reference('patients')
    return ref.get() or []  # Return the patients or an empty list if none found

def get_patient_file_path(name):
    """Generates a reference path for the patient's data in Firebase."""
    return f'patients/{name}'

def create_patient(name):
    """Creates a new patient record in Firebase if it does not exist."""
    ref = db.reference(get_patient_file_path(name))
    if ref.get() is None:  # Check if patient already exists
        ref.set({"name": name, "records": []})

def load_patient(name):
    """Loads patient data from Firebase."""
    try:
        ref = db.reference(get_patient_file_path(name))
        data = ref.get()
        if data is None:
            raise ValueError("No data found for this patient.")
        
        # Ensure that 'records' exists in the data
        if 'records' not in data:
            data['records'] = []
        
        return data
    except Exception as e:
        print(f"Error loading patient data: {e}")
        return {"name": name, "records": []}

def save_patient(name, data):
    """Saves the patient data to Firebase."""
    ref = db.reference(get_patient_file_path(name))
    ref.set(data)

def add_patient_visit(name,age,gender,contact, next_of_kin,chief_complain, hpc, pdh, pmh, diagnosis, treatment , management, amount_charged, medicine, amount_paid, balance):
    """Adds a visit record for a patient."""
    # Calculate the balance
    balance = amount_charged - amount_paid
    
    # Create a patient record dictionary
    patient_record = {
        'age':age,
        'gender':gender,
        'contact':contact,
        'next_of_kin':next_of_kin,
        'chief_complain':chief_complain,
        'hpc':hpc,
        'pdh':pdh,
        'pmh':pmh,
        'diagnosis':diagnosis,
        'treatment': treatment,
        'management': management,
        'amount_charged': amount_charged,
        'amount_paid': amount_paid,
        'balance': balance,
        'medication': medicine,
        # Removed 'date' field as per your request
    }
    
    # Reference to the patient's node in Firebase
    ref = db.reference(get_patient_file_path(name))
    
    # Append the new visit record to the existing records
    current_data = ref.get() or {"name": name, "records": []}
    
    # Ensure 'records' is initialized
    if 'records' not in current_data:
        current_data['records'] = []
    
    current_data['records'].append(patient_record)
    
    # Save the updated patient data back to Firebase
    ref.set(current_data)
    print(f"Patient visit for {name} added successfully.")

def delete_patient(name):
    """Deletes a patient record from Firebase."""
    ref = db.reference(get_patient_file_path(name))
    ref.delete()











