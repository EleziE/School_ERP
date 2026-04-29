from odoo import api, fields, models

class MyProfileTeacher(models.Model):
    _name = 'my.profile.teacher'

    user_id = fields.Many2one(comodel_name='res.users',readonly=True)
    teacher_id = fields.Many2one(comodel_name='teacher.teacher', compute='_compute_teacher_id',store=True)
    name = fields.Char(related='teacher_id.name',store=True)
    surname = fields.Char(related='teacher_id.surname',store=True)
    phone = fields.Char(related='teacher_id.phone',store=True)
    dob = fields.Date(related='teacher_id.dob',store=True)
    education = fields.Selection(related='teacher_id.education',store=True)
    blood_type = fields.Selection(related='teacher_id.blood_type',store=True)
    subject_id = fields.Many2many(comodel_name='subject.subject',store=True)
    class_room_id = fields.Many2many(comodel_name='class.rooms',store=True)
    member_type = fields.Selection(related='user_id.member_type',store=True)
    sequence = fields.Char(related='teacher_id.sequence',store=True)
    gender = fields.Selection(related='teacher_id.gender',store=True)
    email = fields.Char(related='teacher_id.email',store=True)



    # Autofill the fields
    @api.depends('user_id')
    def _compute_teacher_id(self):
        logged_user = self.env.user.id
        for rec in self:
             rec.teacher_id = self.env['teacher.teacher'].search([('user_id', '=', logged_user)], limit=1).id

    def action_print_report(self):
        """
        To Generate the report and take the information in a PDF
        """
        report = self.env['person.profile.information.report']
        pdf_base64 = report.generate_my_profile(self)

        attachment = self.env['ir.attachment'].create({
            'name': f'Teacher_Profile_{self.name}.pdf',
            'type': 'binary',
            'datas': pdf_base64,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }
