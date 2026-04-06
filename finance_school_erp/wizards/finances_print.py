from odoo import models, fields
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import io
import base64

class FinanceReportWizard(models.TransientModel):
    _name = 'finance.report.wizard'
    _description = 'Finance Report Wizard'

    # Wizard fields
    student_id = fields.Many2one('students.students', string="Student")
    date_start = fields.Date("Start Date")
    date_end = fields.Date("End Date")
    pdf_file = fields.Binary("Report")
    pdf_filename = fields.Char(default="finance_report.pdf")

    def action_generate_report(self):
        self.ensure_one()

        # Prepare domain to filter finance records
        domain = []
        if self.student_id:
            domain.append(('student_id', '=', self.student_id.id))
        if self.date_start:
            domain.append(('create_date', '>=', self.date_start))
        if self.date_end:
            domain.append(('create_date', '<=', self.date_end))

        records = self.env['finance.finance'].search(domain)

        # Prepare table data for PDF
        table_data = [["Date", "Amount", "Status"]]
        for rec in records:
            state_label = dict(rec._fields['state'].selection).get(rec.state)
            table_data.append([
                str(rec.create_date.date()),
                str(rec.amount),
                state_label
            ])

        # Generate PDF
        pdf_base64 = self._generate_pdf(table_data)

        # Save PDF in wizard record
        self.write({
            'pdf_file': pdf_base64,
            'pdf_filename': "finance_report.pdf"
        })

        # Return download URL
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/finance.report.wizard/{self.id}/pdf_file/finance_report.pdf?download=true',
            'target': 'self',
        }

    def _generate_pdf(self, table_data):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        elements = []
        elements.append(Paragraph("Finance Report", styles["Title"]))
        elements.append(Spacer(1, 12))

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))

        elements.append(table)
        doc.build(elements)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        return base64.b64encode(pdf_bytes)