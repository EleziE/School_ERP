from odoo import fields, models


class Student(models.Model):
    _name = 'students.students'
    _description = 'Students'

    user_id = fields.Many2one(comodel_name='res.users')
    name = fields.Char(string='Name',related='user_id.name',readonly=True)
    gender = fields.Selection(string='Gender', related='user_id.gender',readonly=False)
    dob = fields.Date(string='Date of birth',related='user_id.dob',readonly=True)
    blood_type = fields.Selection(string='Blood type',related='user_id.blood_type',readonly=True)
    email = fields.Char(string='Email',related='user_id.email',readonly=True)
    classroom_id = fields.Many2one(comodel_name='class.rooms', string='Class')
    subject_id = fields.Many2many(comodel_name='subject.subject')
    state = fields.Selection(selection=[('active', 'Active'),
                                        ('inactive', 'Not Active'),
                                        ('suspended', 'Suspended'),
                                        ('graduated', 'Graduated'),
                                        ('draft', 'Draft'),
                                        ('rejected', 'Rejected'), ],
                             string='Status',
                             default='draft')
    suspend_reason = fields.Text(string='Suspension Reason')
    phone = fields.Char(string='Phone no ', related='user_id.phone')

    def action_open_suspend_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Suspend Student',
            'res_model': 'suspend_reason_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

    def action_draft(self):
        self.state = 'draft'

    def action_rejected(self):
        self.state = 'rejected'

    def action_graduated(self):
        self.state = 'graduated'

    def action_active(self):
        self.state = 'active'

    def action_inactive(self):
        self.state = 'inactive'

    def action_suspended(self):
        self.state = 'suspended'


class User(models.Model):
    _inherit = 'res.users'

    dob = fields.Date(string='Date of birth')
    gender = fields.Selection(string='Gender',
                              selection=[('female', 'Female'),
                                         ('male', 'Male')])
    blood_type = fields.Selection(selection=[('a+', 'A+'),
                                             ('a-', 'A-'),
                                             ('b+', 'B+'),
                                             ('b-', 'B-'),
                                             ('ab+', 'AB+'),
                                             ('ab-', 'AB-'),
                                             ('o+', 'O+'),
                                             ('o-', 'O-'),
                                             ],
                                  string='Blood Type')
