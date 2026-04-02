from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, AccessError


class Teacher(models.Model):
    _name = 'teacher.teacher'
    _description = 'Teacher'

    user_id = fields.Many2one(comodel_name='res.users',
                              required=True)
    name = fields.Char(string='Name',
                       related="user_id.name",
                       store=True,
                       readonly=True)
    surname = fields.Char(string='Surname')
    phone = fields.Char(string='Phone',
                        related="user_id.phone",
                        readonly=True)
    dob = fields.Date(string='Date of birth')
    education = fields.Selection(selection=[('bachelor', 'Bachelor'),
                                            ('master', 'Master'),
                                            ('doctorate', 'Doctorate')],
                                 string='Education')
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
    gender = fields.Selection(string='Gender',
                              selection=[('female', 'Female'),
                                         ('male', 'Male')], )

    subject_id = fields.Many2many(comodel_name='subject.subject')
    class_room_id = fields.Many2many(comodel_name='class.rooms')
    member_type = fields.Selection(related='user_id.member_type',
                                   readonly=True)
    sequence = fields.Char(string='Teacher ID: ',
                           readonly=True,
                           default=lambda self: _('New'))

    @api.constrains('dob')
    def check_dob(self):
        for rec in self:
            today = fields.Date.today()
            if rec.dob and rec.dob > today:
                raise ValidationError("Date of birth  can't be in the future")


    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('teacher.teacher') or _('New')

        return super().create(vals)

    @api.constrains('user_id')
    def _check_user_not_student(self):
        for rec in self:
            if rec.user_id and rec.user_id.member_type == 'student':
                raise ValidationError(
                    f"'{rec.user_id.name}' is already a Student and cannot be a Teacher."
                )

    ########################### Security for field #########################
    '''
    Only Admins can edit this field
    Not other groups
    '''

    def write(self, vals):
        restricted_fields = [
            'blood_type', 'user_id', 'name', 'surname', 'phone', 'dob',
            'enrollment_date', 'education', 'subject_id', 'class_room_id',
            'sequence', 'member_type'
        ]
        if any(f in vals for f in restricted_fields):
            if not self.env.user.has_group('base_school_erp.group_school_admin'):
                raise AccessError("You can't edit these fields.")
        return super().write(vals)


    @api.model
    def open_my_profile(self):
        """
        Return action that opens the logged-in teacher's profile
        Made with pure ChatGPT how I don't know hy hy hy
        """
        teacher = self.env['teacher.teacher'].search([('user_id', '=', self.env.uid)],limit=1)
        if not teacher:
            teacher = self.create({'user_id': self.env.uid})
        return{
            'type': 'ir.actions.act_window',
            'name': 'My Profile',
            'res_model': 'teacher.teacher',
            'res_id': teacher.id,
            'view_mode': 'form',
            'target': 'current',
            'views': [(self.env.ref('teacher_school_erp.my_profile_teacher').id, 'form')],
        }

class Student(models.Model):
    _inherit = 'students.students'

    teacher_ids = fields.Many2many(comodel_name='teacher.teacher',
                                   relation='teacher_student',
                                   column1='student',
                                   column2='teacher',
                                   compute='_compute_teacher',
                                   readonly=True)

    @api.onchange('classroom_id')
    def _compute_teacher(self):
        teachers = self.env['teacher.teacher'].search([('class_room_id', 'in', self.classroom_id.id)])
        self.teacher_ids = teachers
