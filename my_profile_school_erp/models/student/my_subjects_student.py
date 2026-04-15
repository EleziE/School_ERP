from odoo import fields, models,api


class MySubjects(models.Model):
    _name = 'my.subject.student'
    _rec_name = 'name'

    user_id = fields.Many2one(comodel_name='res.users')
    student_id = fields.Many2one(comodel_name='students.students')
    subject_id = fields.Many2one(comodel_name='subject.subject')

    name = fields.Char(string='Name', related='student_id.name')
    faculty_name = fields.Selection(string='Faculty ', related='subject_id.faculty')
    year = fields.Selection(string='Year', related='subject_id.year')
    type = fields.Selection(string='Type', related='subject_id.type')
    credits = fields.Integer(string='Credits', related='subject_id.credits')
    semester = fields.Selection(string='Semester', related='subject_id.semester')
    sub_seq = fields.Char(string="Subject ID", related='subject_id.sequence')


    @api.onchange('user_id')
    def _compute_student_id(self):
        """
        Autofill the fields
        """
        logged_user = self.env.user.id
        for rec in self:
            rec.student_id = self.env['my.subject.student'].search([('user_id', '=', logged_user)], limit=1).id
