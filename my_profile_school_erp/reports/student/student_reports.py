from odoo import api, fields, models, tools
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import base64
import io

def my_finances_report(user_name, state, finances):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    finances = ['']
    elements = []

    elements.append(Paragraph('"Finances Report"', styles["Title"]))
    elements.append(Paragraph(f"User name: {user_name}", styles["Normal"]))
    elements.append(Paragraph(f"State: {state}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    for finance in finances:
        elements.append(Paragraph(f"- {finance}", styles["Normal"]))
        elements.append(Spacer(1, 8))

    doc.build(elements)

    pdf_bytes = buffer.getvalue()

    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

    print(pdf_base64)
