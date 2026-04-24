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

# For the finances_print_wizard report

class ReportFinances(models.AbstractModel):
    _name = 'report.finances.report'
    _description = 'ReportLab Finances Report'


    def print_finances_report(record):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        element = []

        dob_formatted = record.dob.strftime("%d/%m/%Y") if record.dob else ''

        def add_footer_header(canvas,_doc ):
            canvas.saveState()

            # Header
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

        if record.member_type == 'student':

            element.drawString(Paragraph("Finances Report",styles["Normal"]))
            element.append(Spacer(1, 12))
            element.append(Paragraph(f"Student ID: {record.id}", styles['Normal']))
            element.append(Spacer(1, 6))
            element.append(Paragraph(f"Name : {record.name}", styles['Normal']))
            element.append(Spacer(1, 6))
            element.append(Paragraph(f"Surname : {record.surname}", styles['Normal']))

        table_data = [['Reason','State','Amount']]
        for reason,state,amount in payment_details:
            print_date_formated = paid_date.strftime("%d/%m/%Y") if paid_date else ''
            table_data.appent([
                str(reason or ''),
                str(state or ''),
                str(amount or '')
            ])
        table = Table(table_data, style=styles['Table'])

        doc.build(element,
                  onFirstPage=add_footer_header,
                  onLaterPages=add_footer_header)
        pdf = buffer.getvalue()
        buffer.close()

        return base64.b64encode(pdf)
