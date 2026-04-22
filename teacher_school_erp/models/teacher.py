from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, AccessError


class Teacher(models.Model):
    _name = 'teacher.teacher'
    _description = 'Teacher'
    _inherit = ['mail.thread','mail.activity.mixin']

    user_id = fields.Many2one(comodel_name='res.users',
                              required=True,)
    sequence = fields.Char(string='Teacher ID: ',
                           readonly=True,
                           default=lambda self: _('New'))
    name = fields.Char(string='Name',
                       store=True,
                       tracking=True)
    surname = fields.Char(string='Surname',
                          store=True,
                       tracking=True)
    phone = fields.Char(string='Phone',
                        store=True,)
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
    subject_id = fields.Many2many(comodel_name='subject.subject')
    class_room_id = fields.Many2many(comodel_name='class.rooms')
    member_type = fields.Selection(related='user_id.member_type',
                                   readonly=True)
    gender = fields.Selection(string='Gender',
                              selection=[('female', 'Female'),
                                         ('male', 'Male')], )
    email = fields.Char(string='Email',related='user_id.login',
                        required=True)
    external_email = fields.Char(string='External Email',
                                 help='The email that is personal not the one that we use to log in')

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('teacher.teacher')

        if not vals.get('email'):
            raise ValueError("Email is a must, it can't be left empty !!!")

        if not vals.get('name'):
            raise ValueError("Name is a must, it can't be left empty !!!")


        access_rights = self.env.ref('base_school_erp.group_school_teacher')
        internal_user = self.env.ref('base.group_user')


        user = self.env['res.users'].create({
            'name': vals.get('name'),
            'login':vals.get('email'),
            'member_type':'teacher',
            'groups_id':[
                (4,access_rights.id),
                (4,internal_user.id),]
        })
        vals ['user_id'] = user.id
        return super().create(vals)

    def write(self, vals):
        """
        Only Admins can edit this field
        Not other groups
        """
        restricted_fields = [
            'blood_type', 'user_id', 'name', 'surname', 'phone', 'dob',
            'enrollment_date', 'education', 'subject_id', 'class_room_id',
            'sequence', 'member_type'
        ]
        if any(f in vals for f in restricted_fields):
            if not (self.env.user.has_group('base_school_erp.group_school_admin')
                    or self.env.user.has_group('base_school_erp.group_school_administration')):
                raise AccessError("You can't edit these fields.")
        return super().write(vals)

    @api.constrains('user_id')
    def _check_user_not_student(self):
        for rec in self:
            if rec.user_id and rec.user_id.member_type == 'student':
                raise ValidationError(
                    f"'{rec.user_id.name}' is already a Student and cannot be a Teacher."
                )

    @api.constrains('dob')
    def check_dob(self):
        for rec in self:
            today = fields.Date.today()
            if rec.dob and rec.dob > today:
                raise ValidationError("Date of birth  can't be in the future")



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

