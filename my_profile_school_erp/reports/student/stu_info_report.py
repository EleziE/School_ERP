from odoo import models
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
import base64


class StudentProfileReport(models.AbstractModel):
    _name = 'student.info.report'

    @staticmethod
    def generate_pdf(record):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        elements = []

        elements.append(Paragraph("Student Profile Report", styles['Title']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Student Information", styles['Heading2']))
        elements.append(Paragraph(f"Student No: {(record.sequence or '').capitalize()}", styles['Normal']))
        elements.append(Paragraph(f"Name: {(record.name or '').capitalize()}", styles['Normal']))
        elements.append(Paragraph(f"Surname: {(record.surname or '').capitalize()}", styles['Normal']))
        elements.append(Paragraph(f"Date of Birth: {record.dob or ''}", styles['Normal']))
        elements.append(Paragraph(f"State: {(record.state or '').capitalize()}", styles['Normal']))
        elements.append(Paragraph(f"Email: {record.email or ''}", styles['Normal']))
        elements.append(Paragraph(f"Enrollment Date: {record.enrollment_date or ''}", styles['Normal']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Finance Records", styles['Heading2']))

        if record.finance_ids:

            data = [["Amount", "Reason", "State"]]

            for finance in record.finance_ids:
                data.append([
                    finance.amount,
                    finance.reason.capitalize() if finance.reason else "",
                    finance.state.capitalize() if finance.state else "",
                ])

            # 👉 IMPORTANT: force full page width
            page_width = 500  # typical usable width in portrait A4 (adjust if needed)

            table = Table(
                data,
                colWidths=[page_width * 0.2, page_width * 0.5, page_width * 0.3]
            )

            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]))

            elements.append(table)

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