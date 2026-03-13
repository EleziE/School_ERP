from odoo import fields, models

class AssignClassroomWizard(models.TransientModel):
    _name = 'assign.classroom.wizard'
    _description = 'Assign Students to Classroom'

    classroom_id = fields.Many2one(comodel_name='class.rooms',
                                   string='Classroom',
                                   required=True)
    student_ids = fields.Many2many(comodel_name='students.students')

    def action_assign(self):
        for student in self.student_ids:
            student.classroom_id = self.classroom_id