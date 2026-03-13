from odoo import  fields, models

class AssignSubjectTeacherWizard(models.TransientModel):
    _name = 'subject.teacher.wizard'

    teacher_id = fields.Many2one(comodel_name='teacher.teacher',)
    subject_id =fields.Many2one(comodel_name='subject.subject')

    def action_assign(self):
        self.teacher_id.subject_id = [(4, self.teacher_id.id)]
