from odoo import fields, models
import base64
from odoo.exceptions import UserError
# Import the function we created in the other file
from ..reports.payment_report import generate_student_finance_pdf


class PrintFinancesWizard(models.TransientModel):
    _name = 'print.paid.finances.wizard'
    _description = 'Print Finances Wizard'
    """
    We select the status of the payment and based on that we retrive a pdf with payments.
    "All" - retrives all the types of payments .
    If the state you have selected doesnt exist , an 'No record found' will be displayed .
    """

    student_id = fields.Many2one('students.students', string="Student", readonly=True)
    finance_id = fields.Many2one('finance.finance', string="Finance Reference")
    start_date = fields.Datetime(string="Start Date", related='finance_id.create_date')

    state = fields.Selection(
        selection=lambda self: self.env['finance.finance']._fields['state'].selection,
        string="Report Status",
        default='paid',
        required=True
    )

    def action_print_report(self):
        self.ensure_one()

        domain = [('student_id', '=', self.student_id.id)]

        if self.state != 'all':
            domain.append(('state', '=', self.state))

        payment = self.env['finance.finance'].search(domain)

        if not payment:
            raise UserError('No records found')

        pdf_content = generate_student_finance_pdf(self.student_id, payment)

        attachment = self.env['ir.attachment'].create({
            'name': f'Payment_of_{self.student_id.name}_{self.state}.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'mimetype': 'application/pdf',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
