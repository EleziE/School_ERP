from odoo import fields,models


class Student(models.Model):
    _name = 'students.students'


    name = fields.Char(string='Name')
    surname = fields.Char(string='Surname')
    gender = fields.Selection(string='Gender',selection=[('female','Female'),('male','Male')])
    dob = fields.Date(string='Date of birth')
    blood_type = fields.Char(string='Blood type')
    email = fields.Char(string='Email')
    classroom_id = fields.Many2one(comodel_name='class.rooms',string='Class')

    subject_ids = fields.Many2many(comodel_name='subject.subject')


