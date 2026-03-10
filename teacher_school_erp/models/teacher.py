from odoo import fields,models,api


class Teacher(models.Model):
    _name = 'teacher.teacher'

    name = fields.Char(string='Name')
    surname = fields.Char(string='Surname')
    dob = fields.Date(string='Date of birth')

    subject_id = fields.Many2many(comodel_name='subject.subject')
    class_room_id = fields.Many2many(comodel_name='class.rooms')
    student_id = fields.Many2one(comodel_name='students.students')

class Student(models.Model):
    _inherit = 'students.students'

    teacher_id = fields.One2many(comodel_name='teacher.teacher', inverse_name='student_id')
