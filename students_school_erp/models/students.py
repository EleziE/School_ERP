from odoo import fields, models


class Student(models.Model):
    _name = 'students.students'

    user_id = fields.Many2one(comodel_name='res.users')
    name = fields.Char(string='Name',
                       related='user_id.name',
                       readonly=True)
    gender = fields.Selection(string='Gender',
                              selection=[('female', 'Female'),
                                         ('male', 'Male')],)
    dob = fields.Date(string='Date of birth')
    blood_type = fields.Char(string='Blood type')
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

