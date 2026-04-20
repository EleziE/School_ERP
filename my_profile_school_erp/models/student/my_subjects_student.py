from odoo import fields, models,api


class MySubjects(models.Model):
    _name = 'my.subject.student'
    _rec_name = 'name'

    user_id = fields.Many2one(comodel_name='res.users')
    student_id = fields.Many2one(comodel_name='students.students',compute='_compute_student_id',store=True)
    subject_ids = fields.Many2many(comodel_name='subject.subject')

    faculty_name = fields.Selection(related='student_id.faculty',readonly=False)
    year = fields.Selection(related='student_id.year',readonly=False)
    semester = fields.Selection(related='student_id.subject_id.semester',readonly=False)

    coursers_subject = fields.Many2many(comodel_name='subject.subject',compute='_compute_courses_subject')


    name = fields.Char(related='student_id.name')
    type = fields.Selection( related='student_id.subject_id.type')
    credits = fields.Integer(related='student_id.subject_id.credits')
    sub_seq = fields.Char(related='student_id.subject_id.sequence')

    @api.onchange('user_id')
    def _compute_student_id(self):
        """
        Autofill the fields
        """
        for rec in self:
            rec.student_id = self.env['students.students'].search([('user_id', '=', self.env.user.id)], limit=1).id

    @api.depends('year','semester','faculty_name')
    def _compute_courses_subject(self):
        for rec in self:
            if rec.year and rec.semester and rec.faculty_name:
                rec.coursers_subject = self.env['subject.subject'].search([
                    ('year', '=', rec.year),
                    ('semester', '=', rec.semester),
                    ('faculty', '=', rec.faculty_name),
                ])
            else:
                rec.coursers_subject = False