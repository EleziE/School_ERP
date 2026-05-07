from odoo import models
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import base64


class FinanceSelection(models.AbstractModel):
    _name = 'finance.selection.report'
    _description = 'Finance Selection Report'

    def generate_fiance_report(self, record):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        elements = []
        elements.append(Paragraph(f"{record.name} Finance Report ({record.state})", styles['Title']))
        elements.append(Spacer(1, 12))

        for record in record:
            if record.state == 'paid':
                elements.append(Paragraph(f'{record.state}', 12))

            if record.state == 'unpaid':
                elements.append(Paragraph(f'{record.state}', 12))


        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()

        return base64.b64encode(pdf)