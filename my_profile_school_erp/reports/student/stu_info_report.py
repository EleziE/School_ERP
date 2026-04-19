from odoo import models
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import base64


class TeacherProfileReport(models.AbstractModel):
    _name = 'student.info.report'

    def generate_pdf_student(self, record):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        elements = []
        elements.append(Paragraph("Student Profile Report", styles['Title']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Student Information", styles['Heading2']))
        elements.append(Paragraph(f"Student No: {record.sequence or ''}", styles['Normal']))
        elements.append(Paragraph(f"Name: {record.name or ''}", styles['Normal']))
        elements.append(Paragraph(f"Surname: {record.surname or ''}", styles['Normal']))
        elements.append(Paragraph(f"Date of Birth: {record.dob or ''}", styles['Normal']))
        elements.append(Paragraph(f"Email: {record.email or ''}", styles['Normal']))
        elements.append(Spacer(1, 12))

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()

        return base64.b64encode(pdf)