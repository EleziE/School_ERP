from odoo import api, fields, models, tools
from odoo.addons.my_profile_school_erp.reports import reports as rpt

class MyProfileTeacher(models.Model):
    _name = 'my.profile.teacher'

    user_id = fields.Many2one(comodel_name='res.users')
    teacher_id = fields.Many2one(comodel_name='teacher.teacher', compute='_compute_teacher_id')
    name = fields.Char(related='teacher_id.name')
    surname = fields.Char(related='teacher_id.surname')
    phone = fields.Char(related='teacher_id.phone')
    dob = fields.Date(related='teacher_id.dob')
    education = fields.Selection(related='teacher_id.education')
    blood_type = fields.Selection(related='teacher_id.blood_type')
    subject_id = fields.Many2many(comodel_name='subject.subject')
    class_room_id = fields.Many2many(comodel_name='class.rooms')
    member_type = fields.Selection(related='user_id.member_type')
    sequence = fields.Char(related='teacher_id.sequence')
    gender = fields.Selection(related='teacher_id.gender')
    email = fields.Char(related='teacher_id.email')



    # Autofill the fields
    @api.onchange('user_id')
    def _compute_teacher_id(self):
        logged_user = self.env.user.id
        for rec in self:
             rec.teacher_id = self.env['teacher.teacher'].search([('user_id', '=', logged_user)], limit=1).id

    def print_subjects(self):
        for rec in self:
            subject_names = [s.name for s in rec.teacher_id.subject_id]
            username = rec.teacher_id.name
            pdf_base64 = rpt._report_generator(user_name=username,subjects=subject_names)
            print(pdf_base64)
            # rec.pdf_file = pdf_base64
            # rec.pdf_filename = "subjects.pdf"
            #
            # return {
            #     'type': 'ir.actions.act_url',
            #     'url': f'/web/content/{rec._name}/{rec.id}/pdf_file/{rec.pdf_filename}?download=true',
            #     'target': 'self',
            # }