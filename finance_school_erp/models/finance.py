from odoo import fields, models, api


class Finance(models.Model):
    _name = 'finance.finance'
    _description = 'Finance'
    _rec_name = 'student_id'

    created_by = fields.Many2one(comodel_name='res.users',
                                 string='Created by',
                                 default=lambda self: self.env.user,
                                 readonly=True)

    created_by_info = fields.Char(string='Created by',
                                  compute='_compute_created_by_info')

    amount = fields.Float(string='Amount')
    reason = fields.Char(string='Reason',
                         required=True,
                         help='Reason for payment',
                         default='No reason')
    state = fields.Selection(string='State',
                             selection=[('draft', 'Draft'),
                                        ('paid', 'Paid'),
                                        ('unpaid', 'Unpaid')],
                             default='draft')
    student_id = fields.Many2one(comodel_name='students.students',
                                 string='Student')

    paid_date = fields.Datetime(string='Paid Date', compute='_compute_paid_date',
                                readonly=True,
                                store=True)

    # def write(self, vals):
    #     if 'state' in vals and vals['state'] == 'paid':
    #         for rec in self:
    #             if not rec.paid_date:
    #                 rec.paid_date = fields.Datetime.now()
    #     return super().write(vals)

    @api.depends('state')
    def _compute_paid_date(self):
        """
        Pse ma ruan ne te njejten time (date tmm ama time pse nuk ndryshon)
        """
        for record in self:
            if record.state == 'paid':
                record.paid_date = fields.Datetime.now()
            else:
                record.paid_date = False

    @api.depends('created_by')
    def _compute_created_by_info(self):
        for rec in self:
            if rec.created_by:
                name = rec.created_by.name
                email = rec.created_by.login or 'N/A'
                rec.created_by_info = f"{name} -> {email}"
            else:
                rec.created_by_info = 'N/A'

    def my_finance_student(self):
        user = self.env.user.id
        # records = self.search([('created_by', '=', user)]) NOT NEEDED DOMAIN DOES ITS JOB !!! (in this case)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'finance.finance',
            'view_mode': 'tree,form',
            'domain': [('created_by', '=', user)],
            'name': 'My Finances',
        }

    def pay_finance(self):
        self.state = 'paid'
        print(f'{self.student_id.name} paid the payment of {self.amount} LEK (te reja)!')

    def unpaid_finance(self):
        self.state = 'unpaid'
        print(f'{self.student_id.name} has to make the payment of {self.amount} LEK (te reja)!')


class Student(models.Model):
    _inherit = 'students.students'

    finance_ids = fields.One2many(comodel_name='finance.finance',
                                  inverse_name='student_id',
                                  string='Finances')
