from odoo import fields, models, api, _
from odoo.exceptions import UserError
import secrets


class Finance(models.Model):
    _name = 'finance.finance'
    _description = 'Finance'
    _rec_name = 'student_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one(comodel_name='res.users')

    sequence = fields.Char(string='Records ID: ',
                           readonly=True)

    create_uid = fields.Many2one(comodel_name='res.users',
                                 string='Created by',
                                 default=lambda self: self.env.user,
                                 readonly=True)

    create_uid_info = fields.Char(string='Created by (Info)',
                                  compute='_compute_create_uid_info')

    amount = fields.Float(string='Amount')

    reason = fields.Selection(string='Reason',
                              required=True,
                              help='Reason for payment',
                              selection=[
                                  ('first_semester_payment_1year', 'Spring Semester Payment (First-Year)'),
                                  ('first_semester_payment_2year', 'Spring Semester Payment (Second-Year)'),
                                  ('first_semester_payment_3year', 'Spring Semester Payment (Third-Year)'),
                                  ('second_semester_payment_1year', 'Fall Semester Payment (First-Year)'),
                                  ('second_semester_payment_2year', 'Fall Semester Payment (Second-Year)'),
                                  ('second_semester_payment_3year', 'Fall Semester Payment (Third-Year)'),
                                  ('extra_credits', 'Extra Credits'),
                                  ('transportation_fee', 'Transportation Fee'), ])
    reason_extra = fields.Char(string='Extra Reason')
    student_number = fields.Char(string='Student ID',
                                 related='student_id.sequence')

    state = fields.Selection(string='State',
                             selection=[('draft', 'Draft'),
                                        ('unpaid', 'Unpaid'),
                                        ('paid', 'Paid')],
                             default='draft',
                             tracking=True)
    student_id = fields.Many2one(comodel_name='students.students',
                                 string='Student',
                                 required=True)
    student_seq = fields.Char(string='Student Sequence',
                              related='student_id.sequence')
    paid_date = fields.Datetime(string='Paid Date',
                                compute='_compute_paid_date',
                                readonly=True,
                                store=True)
    confirmed_by = fields.Char(string='Confirmed By',
                               compute='_compute_confirmed_by',
                               store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', _('New')) == _('New'):
                vals['sequence'] = self._generate_unique_sequence()

        # Always pass the entire list to super()
        return super().create(vals_list)

    def _generate_unique_sequence(self):
        while True:
            number = str(secrets.randbelow(9000000) + 1000000)
            sequence = f'FIN-{number}'
            existing = self.search([('sequence', '=', sequence)], limit=1)
            if not existing:
                return sequence

    def write(self, vals):
        readonly_fields = {'student_id', 'paid_date', 'amount'}

        for rec in self:
            if rec.state == 'paid' and (readonly_fields & set(vals.keys())):
                raise UserError("Paid records cannot be modified.")

        return super().write(vals)

    @api.depends('user_id', 'state')
    def _compute_confirmed_by(self):
        for rec in self:
            if rec.state == 'paid' and rec.user_id:
                rec.confirmed_by = rec.user_id.name
            else:
                rec.confirmed_by = False

    @api.depends('state')
    def _compute_paid_date(self):
        for record in self:
            if record.state == 'paid':
                record.paid_date = fields.Datetime.now()
            else:
                record.paid_date = False

    @api.depends('create_uid')
    def _compute_create_uid_info(self):
        for rec in self:
            if rec.create_uid:
                name = rec.create_uid.name
                email = rec.create_uid.login or 'N/A'
                rec.create_uid_info = f"{name} -> {email}"
            else:
                rec.create_uid_info = 'N/A'

    def my_finance_student(self):
        user = self.env.user.id
        # records = self.search([('create_uid', '=', user)]) NOT NEEDED DOMAIN DOES ITS JOB !!! (in this case)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'finance.finance',
            'view_mode': 'tree,form',
            'domain': [('create_uid', '=', user)],
            'name': 'My Finances',
        }

    def pay_finance(self):
        self.write({
            'state': 'paid',
            'user_id': self.env.user.id,
        })

    def unpaid_finance(self):
        self.state = 'unpaid'


class Student(models.Model):
    _inherit = 'students.students'

    finance_ids = fields.One2many(comodel_name='finance.finance',
                                  inverse_name='student_id',
                                  string='Finances')
