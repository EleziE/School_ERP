from odoo import fields, models,api


class MySubjects(models.Model):
    _name = 'my.subject.student'
    _rec_name = 'name'

    user_id = fields.Many2one(comodel_name='res.users')
    student_id = fields.Many2one(comodel_name='students.students',compute='autofill_fields')
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
    def autofill_fields(self):
        """
        Autofill the fields
        """
        for rec in self:
            rec.student_id = self.env['students.students'].search([('user_id', '=', self.env.user.id)], limit=1)
