from tkinter import Tk, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from utils.patients import load_patient, get_all_patients

def export_patient_to_pdf(name):
    """Exports a patient's history to a PDF file chosen by the user."""
    data = load_patient(name)
    if not data or not data.get("records"):
        return False  # No data to export

    # Suggest a safe default filename
    safe_name = name.replace(" ", "_")
    default_filename = f"{safe_name}_history.pdf"

    # Ask user where to save the file
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.asksaveasfilename(
        title="Export Patient History to PDF",
        defaultextension=".pdf",
        initialfile=default_filename,
        filetypes=[("PDF files", "*.pdf")]
    )
    root.destroy()

    if not file_path:
        return None  # User cancelled

    # Create and write PDF
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, f"Patient Record: {data['name']}")

    c.setFont("Helvetica", 12)
    y = 720

    for rec in data["records"]:
        # Format each field in a new line for better readability
        c.drawString(50, y, f"Age: {rec.get('age', 'N/A')}")
        y -= 20
        c.drawString(50, y, f"Gender: {rec.get('gender', 'N/A')}")
        y -= 20
        c.drawString(50, y, f"Contact: {rec.get('contact', 'N/A')}")
        y -= 20
        c.drawString(50, y, f"Next of Kin: {rec.get('next_of_kin', 'N/A')}")
        y -= 20
        c.drawString(50, y, f"Chief Complaint: {rec.get('chief_complain', 'N/A')}")
        y -= 20
        c.drawString(50, y, f"HPC: {rec.get('hpc', 'N/A')}")
        y -= 20
        c.drawString(50, y, f"PDH: {rec.get('pdh', 'N/A')}")
        y -= 20
        c.drawString(50, y, f"PMH: {rec.get('pmh', 'N/A')}")
        y -= 20
        c.drawString(50, y, f"Diagnosis: {rec.get('diagnosis', 'N/A')}")
        y -= 20
        c.drawString(50, y, f"Treatment: {rec.get('treatment', 'N/A')}")
        y -= 20
        c.drawString(50, y, f"Management: {rec.get('management', 'N/A')}")
        y -= 20
        c.drawString(50, y, f"Amount Charged: Ksh{rec.get('amount_charged', 0):.2f}")
        y -= 20
        c.drawString(50, y, f"Amount Paid: Ksh{rec.get('amount_paid', 0):.2f}")
        y -= 20
        c.drawString(50, y, f"Balance: Ksh{rec.get('balance', 0):.2f}")
        y -= 20
        c.drawString(50, y, f"Medication: {rec.get('medication', 'N/A')}")
        y -= 20
        c.drawString(50, y, "-" * 50)  # Separator line
        y -= 10

        # Check if we need to create a new page
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750

    c.save()
    return file_path

# Example usage (uncomment to use):
# if __name__ == "__main__":
#     export_patient_to_pdf("John Doe")








