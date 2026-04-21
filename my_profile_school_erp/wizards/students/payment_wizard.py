from odoo import models,fields

class PaymentWizard(models.TransientModel):
    _name = 'payment.wizard'
    _description = 'Payment Wizard'

    finance_id = fields.Many2one(comodel_name='finance.finance')
    user_id = fields.Many2one(comodel_name='res.users')
    student_id = fields.Many2one(comodel_name='students.students')


    finance_type = fields.Selection(related="finance_id.state")

