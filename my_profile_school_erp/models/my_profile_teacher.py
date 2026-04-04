from odoo import api, fields, models, tools

class MyProfileTeacher(models.Model):
    _name = 'my.profile.teacher'

    user_id = fields.Many2one(comodel_name='res.users')
    teacher_id = fields.Many2one(comodel_name='teacher.teacher')
    name = fields.Char(related='teacher_id.name')
    surname = fields.Char(related='teacher_id.surname')
    phone = fields.Char(related='teacher_id.phone')
    dob = fields.Date(related='teacher_id.dob')
    education = fields.Selection(related='teacher_id.education')
    blood_type = fields.Selection(related='teacher_id.blood_type')
    subject_id = fields.Many2many(comodel_name='subject.subject')
    class_room_id = fields.Many2many(comodel_name='class.rooms')
    member_type = fields.Selection(related='user_id.member_type')
    sequence = fields.Char(related='teacher_id.sequence')
    gender = fields.Selection(related='teacher_id.gender')
    email = fields.Char(related='teacher_id.email')
