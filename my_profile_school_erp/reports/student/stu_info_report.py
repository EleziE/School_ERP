from reportlab.lib import colors

from odoo import models
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import base64


class TeacherProfileReport(models.AbstractModel):
    _name = 'student.info.report'

    def generate_pdf_student(self, record,):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        def add_footer_header(canvas,doc):
            canvas.saveState()

            #Header
            created_date = datetime.now().strftime("%d/%m/%Y")
            canvas.setFont('Times-Roman', 12)
            canvas.setFillColor(colors.grey)
            canvas.drawRightString(
                A4[0] - 1 * cm,
                A4[1] - 1 * cm ,
                f'Created: {created_date}',
            )
            #Footer
            canvas.setFont('Times-Roman', 12)
            canvas.setFillColor(colors.grey)
            canvas.drawCentredString(
                A4[0]/2,
                1 * cm,
                "This document is valid 6 month after the created date!"
            )
            canvas.restoreState()


        #Content
        elements = []
        elements.append(Paragraph("Student Profile Report", styles['Title']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Student Information", styles['Heading2']))
        elements.append(Paragraph(f"Student No: {record.sequence or ''}", styles['Normal']))
        elements.append(Paragraph(f"Name: {record.name or ''}", styles['Normal']))
        elements.append(Paragraph(f"Surname: {record.surname or ''}", styles['Normal']))
        elements.append(Paragraph(f"Date of Birth: {record.dob or ''}", styles['Normal']))
        elements.append(Paragraph(f"Email: {record.email or ''}", styles['Normal']))

        footer_text = "This document is valid 6 months after the created date!"


        doc.build(
            elements,
            onFirstPage=add_footer_header,
            onLaterPages=add_footer_header,)

        pdf = buffer.getvalue()
        buffer.close()

        return base64.b64encode(pdf)