from odoo import api, fields, models, tools


class MyProfileStudent(models.Model):
    _name = 'my.profile.student'

    user_id = fields.Many2one(comodel_name='res.users')
    student_id = fields.Many2one(comodel_name='students.students')

    name = fields.Char(related='student_id.name')
    surname = fields.Char(related='student_id.surname')
    phone = fields.Char(related='student_id.phone')
    dob = fields.Date(related='student_id.dob')
    state = fields.Selection(related='student_id.state')
    blood_type = fields.Selection(related='student_id.blood_type')
    subject_id = fields.Many2many(related='student_id.subject_id')
    classroom_id = fields.Many2one(comodel_name='class.rooms',related='student_id.classroom_id')
    member_type = fields.Selection(related='user_id.member_type')
    sequence = fields.Char(related='student_id.sequence')
    gender = fields.Selection(related='student_id.gender')
    email = fields.Char(related='student_id.email')
    suspend_reason = fields.Text(related='student_id.suspend_reason')
    enrollment_date = fields.Date(related='student_id.enrollment_date')
    graduation_date = fields.Date(related='student_id.graduation_date')
