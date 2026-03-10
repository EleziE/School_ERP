from odoo import fields, models


class Teacher(models.Model):
    _name = 'teacher.teacher'

    name = fields.Char(string='Name')
    surname = fields.Char(string='Surname')
    dob = fields.Date(string='Date of birth')

    subject_id = fields.Many2many(comodel_name='subject.subject')
    class_room_id = fields.Many2many(comodel_name='class.rooms')


class Student(models.Model):
    _inherit = 'students.students'

    teacher_id = fields.Many2many(comodel_name='teacher.teacher',
                                  relation='teacher_student',
                                  column1='student',
                                  column2='teacher',
                                  compute='_compute_teacher',
                                  readonly=True)

    def _compute_teacher(self):
        teachers = self.env['teacher.teacher'].search([('class_room_id', 'in', self.classroom_id.id)])
        self.teacher_id = teachers
