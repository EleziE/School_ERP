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
                       readonly=False,
                       store=True)
    surname = fields.Char(string='Surname',
                          related='user_id.surname',
                          readonly=True,
                          store=True)
    gender = fields.Selection(string='Gender',
                              related='user_id.gender',
                              store=True,
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
    state = fields.Selection(selection=[('new', 'New'),
                                        ('active', 'Active'),
                                        ('inactive', 'Not Active'),
                                        ('suspended', 'Suspended'),
                                        ('graduated', 'Graduated'),
                                        ('rejected', 'Rejected'), ],
                             string='Status',
                             default='new')
    suspend_reason = fields.Text(string='Suspension Reason')
    phone = fields.Char(string='Phone no ',
                        related='user_id.phone',
                        placeholder="+355XX XXX XXXX")
    enrollment_date = fields.Date(string='Enrollment Date',
                                  related='user_id.enrollment_date', )
    member_type = fields.Selection(related='user_id.member_type',
                                   string='Role',
                                   readonly=True, )
    user_password = fields.Char(string='Password',
                                related='user_id.new_password', )

    birthday_certificate = fields.Binary(string='Birthday Certificate')
    birthday_certificate_name = fields.Char(string='File name',
                                            default="Document",
                                            accept="application/pdf,"
                                                   "image/png,"
                                                   "image/jpeg")

    @api.constrains('user_id')
    def _check_user_not_teacher(self):
        for rec in self:
            if rec.user_id and rec.user_id.member_type == 'teacher':
                raise ValidationError(
                    f"'{rec.user_id.name}' is already a Teacher and cannot be a Student."
                )

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('students.students') or _('New')
        return super().create(vals)

    def action_open_suspend_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Suspend Student',
            'res_model': 'suspend_reason_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

    def action_open_my_profile(self):
        student = self.search(['user_id', '=', self.env.uid], limit=1)
        return {
            'type': 'ir.actions.act_window',
            'name': 'My Profile',
            'res_model': 'students.students',
            'view_mode': 'form',
            'target': 'current',
            'res_id': student.id,
            'views': [(self.env.ref('students_school_erp.my_profile_student'))]
        }

    ############################ Buttons ###########################################
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
