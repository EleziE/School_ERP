from odoo import fields, models

class AssignTeacherWizard(models.TransientModel):
    _name = 'assign.teacher.wizard'
    _description = 'Assign Teacher to Students'

    student_ids = fields.Many2many(comodel_name='students.students')

    teacher_id = fields.Many2one(comodel_name='teacher.teacher')


