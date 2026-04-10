from odoo import api, fields, models


class MyProfileStudent(models.Model):
    _name = 'my.profile.student'

    user_id = fields.Many2one(comodel_name='res.users')
    student_id = fields.Many2one(comodel_name='students.students', compute='_compute_student_id')

    name = fields.Char(related='student_id.name')
    surname = fields.Char(related='student_id.surname')
    phone = fields.Char(related='student_id.phone')
    dob = fields.Date(related='student_id.dob')
    state = fields.Selection(related='student_id.state')
    blood_type = fields.Selection(related='student_id.blood_type')
    subject_id = fields.Many2many(related='student_id.subject_id')
    classroom_id = fields.Many2one(comodel_name='class.rooms', related='student_id.classroom_id')
    member_type = fields.Selection(related='user_id.member_type')
    sequence = fields.Char(related='student_id.sequence')
    gender = fields.Selection(related='student_id.gender')
    email = fields.Char(related='student_id.email')
    suspend_reason = fields.Text(related='student_id.suspend_reason')
    enrollment_date = fields.Date(related='student_id.enrollment_date')
    graduation_date = fields.Date(related='student_id.graduation_date')
    finance_ids = fields.One2many(related='student_id.finance_ids')

    @api.onchange('user_id')
    def _compute_student_id(self):
        """
        Autofill the fields
        """
        logged_user = self.env.user.id
        for rec in self:
            rec.student_id = self.env['students.students'].search([('user_id', '=', logged_user)], limit=1).id

    def action_print_report(self):
        """
        To Generate the report with a button in the profile (ogrenci belgisis gibi)
        """
        report = self.env['student.info.report']
        pdf_base64 = report.generate_pdf(self)

        attachment = self.env['ir.attachment'].create({
            'name': f'Student_Profile_{self.name}.pdf',
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
