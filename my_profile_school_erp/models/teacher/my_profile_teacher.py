from odoo import api, fields, models
from odoo.addons.my_profile_school_erp.reports.teacher import tea_info_report as rpt

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

    def print_my_finances(self):
        for rec in self:
            my_finances = self.env['finance.finance'].search([('state','=','unpaid')])
            if my_finances:
                return {
                    'name': rec.teacher_id.name,
                    'state': rec.state,
                    'amount': rec.teacher_id.amount,
                    'create_date': rec.create_date,
                }
            else:
                return {'N/A'}

    def action_print_report(self):
        """
        To Generate the report with a button in the profile (ogrenci belgisis gibi)
        """
        report = self.env['teacher.info.report']
        pdf_base64 = report.generate_pdf_teacher(self)

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
            'target': 'self',
        }