from odoo import fields, models

class AssignSubjectWizard(models.TransientModel):
    _name = 'assign.subject.wizard'
    _description = 'Assign Subject'

    subject_id = fields.Many2one(comodel_name='subject.subject',
                                   string='Subjects',
                                   required=True)

    student_ids = fields.Many2one(comodel_name='students.students')

    def action_assign_subject(self):
        for student in self.student_ids:
            student.subject_id = [(4, self.subject_id.id)]