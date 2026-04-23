from odoo import fields, models


class PrintFinancesWizard(models.TransientModel):
    _name = 'print.finances.wizard'

    student_id = fields.Many2one(comodel_name='students.students', readonly=True)

    start_date = fields.Date()
    last_date = fields.Date()

    def student_finances(self):
        for rec in self:
            payment_details = []
            all_payments = rec.env['finance.finance'].search([('create_date', '>=', rec.start_date),
                                                              ('create_date', '<=', rec.last_date),
                                                              ('student_id', '=', rec.student_id.id)])

            for payment in all_payments:
                payment_details.append([payment.amount, payment.state, payment.paid_date])


