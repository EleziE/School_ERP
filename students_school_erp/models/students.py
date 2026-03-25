from datetime import date

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = 'students.students'
    _description = 'Students'

    # Dont know how i did it (learn python baboo se ske gja per terezi )
    sequence = fields.Char(string='Student ID: ',
                           readonly=True,
                           default=lambda self: _('New'))
    user_id = fields.Many2one(comodel_name='res.users')
    name = fields.Char(string='Name',
                       related='user_id.name',
                       readonly=True,
                       store=True)
    surname = fields.Char(string='Surname',
                          related='user_id.surname',
                          readonly=True,
                          store=True)
    gender = fields.Selection(string='Gender',
                              related='user_id.gender',
                              readonly=True)
    dob = fields.Date(string='Date of birth',
                      related='user_id.dob',
                      readonly=True)
    blood_type = fields.Selection(related='user_id.blood_type',
                                  string='Blood Type',
                                  readonly=True)
    email = fields.Char(string='Email',
                        related='user_id.login',
                        readonly=True)
    classroom_id = fields.Many2one(comodel_name='class.rooms',
                                   string='Class')
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
    phone = fields.Char(string='Phone no ',
                        related='user_id.phone',
                        placeholder="+355XX XXX XXXX")
    enrollment_date = fields.Date(string='Enrollment Date',
                                  related='user_id.enrollment_date',)
    def action_open_suspend_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Suspend Student',
            'res_model': 'suspend_reason_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('students.students') or _('New')
        return super().create(vals)

    ############################ Buttons ###########################################
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

    ############################ Constraints ###########################################
    _sql_constraints = [
        ('unique_student_id', 'UNIQUE (sequence)', 'This Student ID already exists.'),
        ('unique_user_id', 'UNIQUE (user_id)', 'This User ID already exists.'),
        ('dob_check', 'CHECK(dob < CURRENT_DATE)', 'Date of birth must be in the past.')
    ]


class User(models.Model):
    _inherit = 'res.users'

    surname = fields.Char(string='Surname')
    gender = fields.Selection(string='Gender',
                              selection=[('female', 'Female'),
                                         ('male', 'Male')], )
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
    dob = fields.Date(string='Date of birth')
    enrollment_date = fields.Date(string='Enrollment Date')
    member_type = fields.Selection(selection=[('student', 'Student'),
                                              ('teacher', 'Teacher'),
                                              ('administrator', 'Administrator'),])


    @api.onchange('name','surname')
    def _onchange_name_set_login(self):
        if self.name:
            parts = self.name.strip().split()
            if len(parts) >= 2:
                first_initial = parts[0][0].lower()
                surname = parts[-1].lower()
                username = f"{first_initial}.{surname}"
            else:
                username = parts[0].lower()
            self.login = f"{username}@school.com"

    @api.constrains('dob')
    def check_dob(self):
        for rec in self:
            today = date.today()
            if rec.dob and rec.dob > today:
                raise ValidationError("Date of birth  can't be in the future")

    @api.constrains('login')
    def _check_unique_login(self):
        for rec in self:
            duplicate = self.env['res.users'].search([
                ('login', '=', rec.login),
                ('id', '!=', rec.id)
            ])
            if duplicate:
                raise ValidationError(f"The email '{rec.login}' is already in use by another user.")
