from odoo import fields, models


class MyFinanceStudent(models.Model):
    _name = 'my.finance.student'

    user_id = fields.Many2one(comodel_name='res.users',
                              readonly=True)
    student_id = fields.Many2one(comodel_name='finance.finance',
                                 readonly=True)
    created_by = fields.Many2one(related='student_id.created_by',
                                 readonly=True)
    created_by_info = fields.Char(related='student_id.created_by_info',
                                  readonly=True)
    amount = fields.Float(related='student_id.amount',
                          readonly=True)
    reason = fields.Char(related='student_id.reason',
                         readonly=True)
    state = fields.Selection(related='student_id.state')

