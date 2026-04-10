from odoo import models
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import base64


class StudentProfileReport(models.AbstractModel):
    _name = 'student.info.report'

    def generate_pdf(self, record):
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
        elements.append(Paragraph(f"State: {record.state or ''}", styles['Normal']))
        elements.append(Paragraph(f"Email: {record.email or ''}", styles['Normal']))
        elements.append(Paragraph(f"Enrollment Date: {record.enrollment_date or ''}", styles['Normal']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Finance Records", styles['Heading2']))
        if record.finance_ids:
            for finance in record.finance_ids:
                elements.append(Paragraph(f"- Amount: {finance.amount}", styles['Normal']))
                elements.append(Paragraph(f"- Reason: {finance.reason}", styles['Normal']))
                elements.append(Paragraph(f"- State: {finance.state}", styles['Normal']))
        else:
            elements.append(Paragraph("No finance records.", styles['Normal']))

        elements.append(Spacer(1, 12))

        if record.suspend_reason:
            elements.append(Paragraph("Suspend Reason", styles['Heading2']))
            elements.append(Paragraph(record.suspend_reason, styles['Normal']))

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()

        return base64.b64encode(pdf)