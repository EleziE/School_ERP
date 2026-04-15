from odoo import fields, models, api
from odoo.exceptions import UserError


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
                                        ('unpaid', 'Unpaid'),
                                        ('paid', 'Paid')],
                             default='draft')
    student_id = fields.Many2one(comodel_name='students.students',
                                 string='Student',required=True)

    paid_date = fields.Datetime(string='Paid Date', compute='_compute_paid_date',
                                readonly=True,
                                store=True)

    readonly_fields = {'student_id','paid_date','amount','created_by','created_by_info'}

    def write(self, vals):
        for rec in self:
            locked_field = self.readonly_fields & set(vals.keys())
            if locked_field:
                raise UserError(
                    f"You cannot edit after saving the creation!")
        return super().write(vals)

    @api.depends('state')
    def _compute_paid_date(self):
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

    def unpaid_finance(self):
        self.state = 'unpaid'


class Student(models.Model):
    _inherit = 'students.students'

    finance_ids = fields.One2many(comodel_name='finance.finance',
                                  inverse_name='student_id',
                                  string='Finances')
