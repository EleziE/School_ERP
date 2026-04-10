from odoo import models
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

class StudentReport(models.AbstractModel):
    _name = 'report.students_module.student_report_pdf'
    _description = 'Student PDF Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['students.students'].browse(docids)
        return {
            'doc_ids': docids,
            'docs': docs,
            'data': data,
        }

    def generate_pdf(self, student):
        """Generates a PDF for a single student"""
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        pdf.setFont("Helvetica", 12)

        pdf.drawString(50, 800, f"Student Report: {student.name} {student.surname}")
        pdf.drawString(50, 780, f"Email: {student.email or 'N/A'}")
        pdf.drawString(50, 760, f"Phone: {student.phone or 'N/A'}")
        pdf.drawString(50, 740, f"Class: {student.classroom_id.name if student.classroom_id else 'N/A'}")
        pdf.drawString(50, 720, f"Enrollment Date: {student.enrollment_date}")
        pdf.drawString(50, 700, f"State: {student.state}")

        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        return buffer.read()