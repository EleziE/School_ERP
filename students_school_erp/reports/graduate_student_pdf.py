from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from odoo import models
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import io
import base64

class ReportFinances(models.AbstractModel):
    _name = 'report.graduated.stu.info'
    _description = 'ReportLab Graduate Student Information Report'

    def generate(self, record):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        elements = []

        dob_formatted = record.dob.strftime("%d/%m/%Y") if record.dob else ''

        def add_footer_header(canvas, _doc):
            canvas.saveState()

            created_date = datetime.now().strftime("%d/%m/%Y")
            canvas.setFont('Times-Roman', 12)
            canvas.setFillColor(colors.grey)
            canvas.drawRightString(
                A4[0] - 1 * cm,
                A4[1] - 1 * cm,
                f'Created: {created_date}',
            )
            canvas.setFont('Times-Roman', 12)
            canvas.setFillColor(colors.grey)
            canvas.drawCentredString(
                A4[0] / 2,
                1 * cm,
                "This document is valid 6 month after the released date!"
            )
            canvas.restoreState()

        if record.state == 'graduated':
            elements.append(Paragraph("Student Profile Report", styles['Title']))
            elements.append(Spacer(1, 12))
            elements.append(Paragraph("Student Information", styles['Heading2']))
            elements.append(Spacer(1, 20))
            elements.append(Paragraph(f"Student ID : {record.sequence or ''}", styles['Normal']))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"Name : {(record.name or '').capitalize()}", styles['Normal']))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"Surname : {(record.surname or '').capitalize()}", styles['Normal']))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"Father name : {(record.father_name or '').capitalize()}", styles['Normal']))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"Mother name : {(record.mother_name or '').capitalize()}", styles['Normal']))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"Date of Birth : {dob_formatted}", styles['Normal']))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"Email : {record.email or ''}", styles['Normal']))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"External email : {record.external_email or ''}", styles['Normal']))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"Graduated date : {record.graduation_date or ''}", styles['Normal']))

        doc.build(elements,
                  onFirstPage=add_footer_header,
                  onLaterPages=add_footer_header)
        pdf = buffer.getvalue()
        buffer.close()

        return base64.b64encode(pdf)