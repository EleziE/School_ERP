from odoo import models,fields

class PaymentWizard(models.TransientModel):
    _name = 'payment.wizard'
    _description = 'Payment Wizard'

    finance_id = fields.Many2one(comodel_name='finance.finance')
    user_id = fields.Many2one(comodel_name='res.users')
    student_id = fields.Many2one(comodel_name='students.students')


    finance_type = fields.Selection(related="finance_id.state")

    def action_print_finance(self):
        """Print the finance details in a PDF"""
        self.ensure_one()

        data={
            'finance_id': self.finance_id.id,
            'user_id': self.user_id.id,
            'student_id': self.student_id.id,
            'finance_type': self.finance_type.id,
        }
        return self.env.ref('my_profile_school_erp.action_print_report')