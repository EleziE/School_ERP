from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import base64
import io


def _report_generator(user_name, subjects):
    # Create in-memory buffer
    buffer = io.BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Subjects list
    # subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "Computer Science"]
    elements = []

    # Title
    elements.append(Paragraph("Subject List", styles["Title"]))
    elements.append(Paragraph(f"User name: {user_name}", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Add subjects
    for subject in subjects:
        elements.append(Paragraph(f"- {subject}", styles["Normal"]))
        elements.append(Spacer(1, 8))

    # Build PDF into buffer
    doc.build(elements)

    pdf_bytes = buffer.getvalue()

    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

    print(pdf_base64)





