from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class Teacher(models.Model):
    _name = 'teacher.teacher'
    _description = 'Teacher'

    user_id = fields.Many2one(comodel_name='res.users',
                              required=True)
    name = fields.Char(string='Name',
                       related="user_id.name",
                       readonly=True)
    surname = fields.Char(string='Surname',
                          related="user_id.surname", )
    phone = fields.Char(string='Phone',
                        related="user_id.phone",
                        readonly=True)
    dob = fields.Date(string='Date of birth',
                      readonly=True,
                      related='user_id.dob')
    education = fields.Selection(related='user_id.education',
                                 string='Education')
    blood_type = fields.Selection(related='user_id.blood_type', )
    subject_id = fields.Many2many(comodel_name='subject.subject')
    class_room_id = fields.Many2many(comodel_name='class.rooms')
    enrollment_date = fields.Date(string='Enrollment Date',
                                  related='user_id.enrollment_date')
    member_type = fields.Selection(related='user_id.member_type',
                                   readonly=True, )

    sequence = fields.Char(string='Teacher ID: ',
                           readonly=True,
                           default=lambda self: _('New'))

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


class Student(models.Model):
    _inherit = 'students.students'

    teacher_id = fields.Many2many(comodel_name='teacher.teacher',
                                  relation='teacher_student',
                                  column1='student',
                                  column2='teacher',
                                  compute='_compute_teacher',
                                  readonly=True)

    @api.onchange('classroom_id')
    def _compute_teacher(self):
        teachers = self.env['teacher.teacher'].search([('class_room_id', 'in', self.classroom_id.id)])
        self.teacher_id = teachers


class ResUser(models.Model):
    _inherit = 'res.users'

    education = fields.Selection(selection=[('bachelor', 'Bachelor'),
                                            ('master', 'Master'),
                                            ('doctorate', 'Doctorate')],
                                 string='Education')

    member_type = fields.Selection(selection=[('student', 'Student'),
                                              ('teacher', 'Teacher'),
                                              ('administrator', 'Administrator')],
                                   required=True)

    @api.constrains('member_type')
    def _check_role_not_duplicate(self):
        for rec in self:
            if rec.member_type == 'teacher':
                student = self.env['students.students'].search([
                    ('user_id', '=', rec.id)
                ])
                if student:
                    raise ValidationError(
                        f"'{rec.name}' is already registered as a Student and cannot be a Teacher."
                    )

            elif rec.member_type == 'student':
                teacher = self.env['teacher.teacher'].search([('user_id', '=', rec.id)])
                if teacher:
                    raise ValidationError(
                        f"'{rec.name}' is already registered as a Teacher and cannot be a Student."
                    )
