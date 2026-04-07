from odoo import models
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


class FinanceReport(models.AbstractModel):
    _name = 'finance.report'

    def generate_pdf(self, records):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, height - 50, "Finance Report")

        pdf.setFont("Helvetica", 12)
        y = height - 100
        pdf.drawString(50, y, "Student | Date | Amount | Reason | State")
        y -= 20

        for record in records:
            line = f"{record.student_id.name} | {record.date} | {record.amount} | {record.reason} | {record.state}"
            pdf.drawString(50, y, line)
            y -= 20
            if y < 50:
                pdf.showPage()
                y = height - 50

        pdf.save()
        buffer.seek(0)
        return buffer
