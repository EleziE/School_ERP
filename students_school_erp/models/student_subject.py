from odoo import models, fields

class StudentSubject(models.Model):
    _name = 'student.subjects'
    _description = 'Student Subjects'

    user_id = fields.Many2one(comodel_name='res.users')
    student_id = fields.Many2one(comodel_name='students.students')
    subject_id = fields.Many2one(comodel_name='subject.subject')

    student_sequence = fields.Char(string='Student ID',related='student_id.sequence')
    subject_sequence = fields.Char(string='Subject ID',related='subject_id.sequence')

    faculty = fields.Selection(string='Faculty',related='student_id.faculty')
    year = fields.Selection(string='Year',related='student_id.year')
    semester = fields.Selection(string='Semester',related='student_id.semester')

    student_name = fields.Char(string='Student Name',related='student_id.name')
    subject_name = fields.Char(string='Subject Name',related='subject_id.name')