import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from odoo.http import request
import base64

def action_print_unpaid_pdf(self):
    self.ensure_one()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("Unpaid Finance Report", styles['Title']))
    elements.append(Spacer(1, 12))

    # Filter unpaid finances
    unpaid = self.finance_ids.filtered(lambda f: f.state == 'unpaid')

    # Table data
    data = [["Amount", "Reason"]]

    total = 0

    for f in unpaid:
        data.append([
            f.amount,
            (f.reason or "").capitalize()
        ])
        total += f.amount

    # Table
    table = Table(data, colWidths=[200, 300])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Total
    elements.append(Paragraph(
        f"<b>Total to Pay: {total}</b>",
        styles['Heading2']
    ))

    # Build PDF
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    # Return as download
    pdf_base64 = base64.b64encode(pdf)

    attachment = self.env['ir.attachment'].create({
        'name': f'{self.name}_unpaid.pdf',
        'type': 'binary',
        'datas': pdf_base64,
        'mimetype': 'application/pdf',
    })

    return {
        'type': 'ir.actions.act_url',
        'url': f'/web/content/{attachment.id}?download=true',
        'target': 'self',
    }