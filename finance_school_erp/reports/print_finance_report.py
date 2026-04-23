from odoo import models
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import io
import base64


class ReportFinances(models.AbstractModel):
    _name = 'report.finances.report'
    _description = 'ReportLab Finances Report'

    def generate_pdf(self, wizard):

        # -------------------------
        # 1. FETCH DATA
        # -------------------------
        payments = self.env['finance.finance'].search([
            ('create_date', '>=', wizard.start_date),
            ('create_date', '<=', wizard.last_date),
            ('student_id', '=', wizard.student_id.id)
        ])

        data = []
        for p in payments:
            data.append([
                p.amount,
                p.state,
                p.paid_date
            ])

        # -------------------------
        # 2. CREATE PDF
        # -------------------------
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()
        elements = []

        # Title
        title = f"Finance Report - {wizard.student_id.name}"
        elements.append(Paragraph(title, styles["Title"]))
        elements.append(Spacer(1, 12))

        # Table header
        table_data = [["Amount", "Status", "Date"]]

        for amount, state, date_val in data:

            if isinstance(date_val, datetime):
                date_str = date_val.strftime("%Y-%m-%d %H:%M:%S")
            else:
                date_str = "N/A"

            table_data.append([amount, state, date_str])

        # Table style
        table = Table(table_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]))

        elements.append(table)

        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()

        # -------------------------
        # 3. RETURN DOWNLOAD
        # -------------------------
        attachment = self.env['ir.attachment'].create({
            'name': 'finance_report.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf),
            'res_model': 'print.finances.wizard',
            'res_id': wizard.id,
            'mimetype': 'application/pdf'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }