import io
import base64
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def generate_student_finance_pdf(student, payments):
    """
    Independent function to generate a PDF using ReportLab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    def add_footer_header(c, _doc):
        c.saveState()

        created_date = datetime.now().strftime("%d/%m/%Y")
        c.setFont('Times-Roman', 12)
        c.setFillColor(colors.grey)
        c.drawRightString(
            A4[0] - 1 * cm,
            A4[1] - 1 * cm,
            f'Created: {created_date}',
        )
        c.setFont('Times-Roman', 12)
        c.setFillColor(colors.grey)
        c.drawCentredString(
            A4[0] / 2,
            1 * cm,
            "This document is valid 6 month after the released date!"
        )
        c.restoreState()

    # Title
    elements.append(Paragraph(f"Payment History: {student.sequence}", styles['Title']))
    elements.append(Spacer(1, 20))

    # Table Data
    data = [['Date Paid', 'Reference ID','Status', 'Amount' ]]
    total = 0
    for p in payments:
        data.append([
            str(p.paid_date or ''),
            p.sequence or 'Payment',
            p.state.capitalize(),
            f"{p.amount:,.2f}",
        ])
        total += p.amount

    # Summary Row
    data.append(['TOTAL ','','',f"{total:,.2f}"])

    # Style
    table = Table(data, colWidths=[100, 180, 100, 70])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),
        ('VALIGN', (2, 1), (2, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))

    elements.append(table)
    doc.build(elements,
              onFirstPage=add_footer_header,
              onLaterPages=add_footer_header)

    pdf_content = buffer.getvalue()
    buffer.close()
    return pdf_content