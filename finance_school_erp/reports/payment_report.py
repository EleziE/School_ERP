import io
import base64
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_student_finance_pdf(student, payments):
    """
    Independent function to generate a PDF using ReportLab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph(f"Payment History: {student.name}", styles['Title']))
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
    doc.build(elements)

    pdf_content = buffer.getvalue()
    buffer.close()
    return pdf_content