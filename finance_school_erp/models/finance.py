from odoo import fields,models


class Finance(models.Model):
    _name = 'finance.finance'


    amount = fields.Float(string='Amount')
    state = fields.Selection(string='State',selection=[('draft','Draft'),('paid','Paid'),('unpaid','Unpaid')])

    student_id = fields.Many2one(comodel_name='students.students',string='Student')

    def pay_finance(self):
        self.state = 'paid'
        print(f'Hello {self.student_id.name} have paid you payment of {self.amount}!')

    def unpaid_finance(self):
        self.state = 'unpaid'





class Student(models.Model):
    _inherit = 'students.students'

    finance_ids = fields.One2many(comodel_name='finance.finance',inverse_name='student_id',string='Finances')
