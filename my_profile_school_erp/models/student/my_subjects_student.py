from odoo import fields, models,api


class MySubjects(models.Model):
    _name = 'my.subject.student'
    _rec_name = 'name'

    user_id = fields.Many2one(comodel_name='res.users')
    student_id = fields.Many2one(comodel_name='students.students')
    subject_id = fields.Many2one(comodel_name='subject.subject')

    #To be shown in Form view
    faculty_name = fields.Selection(related='student_id.faculty')
    year = fields.Selection(related='student_id.year')



    name = fields.Char(related='student_id.name')
    type = fields.Selection( related='subject_id.type')
    credits = fields.Integer(related='subject_id.credits')
    semester = fields.Selection(related='subject_id.semester')
    sub_seq = fields.Char(related='subject_id.sequence')

    @api.onchange('user_id')
    def _compute_student_id(self):
        """
        Autofill the fields
        """
        logged_user = self.env.user.id
        for rec in self:
            rec.student_id = self.env['students.students'].search([('user_id', '=', logged_user)], limit=1).id