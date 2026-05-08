from odoo import fields, models
import base64
from odoo.exceptions import UserError
# Import the function we created in the other file
from ..reports.payment import generate_student_finance_pdf


class PrintFinancesWizard(models.TransientModel):
    _name = 'print.paid.finances.wizard'
    _description = 'Print Finances Wizard'

    student_id = fields.Many2one('students.students', string="Student", readonly=True)
    finance_id = fields.Many2one('finance.finance', string="Finance Reference")
    start_date = fields.Datetime(string="Start Date",related='finance_id.create_date')

    state = fields.Selection(
        selection=lambda self: self.env['finance.finance']._fields['state'].selection,
        string="Report Status",
        default='paid',
        required=True
    )

    def action_print_report(self):
        self.ensure_one()

        # 1. Gather data based on the chosen status
        payments = self.env['finance.finance'].search([
            ('student_id', '=', self.student_id.id),
            ('state', '=', self.state),
        ])

        if not payments:
            # Using a user-friendly message
            state_label = dict(self._fields['state'].selection).get(self.state)
            raise UserError(f"No records found for this student with status: {state_label}")

        # 2. Call the separated ReportLab function
        pdf_content = generate_student_finance_pdf(self.student_id, payments)

        # 3. Create attachment and return download
        attachment = self.env['ir.attachment'].create({
            'name': f'Report_{self.student_id.name}_{self.state}.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'mimetype': 'application/pdf',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }