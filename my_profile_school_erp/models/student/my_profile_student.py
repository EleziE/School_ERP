from odoo import api, fields, models


class MyProfileStudent(models.Model):
    _name = 'my.profile.student'
    _description = 'Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    user_id = fields.Many2one(comodel_name='res.users')
    student_id = fields.Many2one(comodel_name='students.students',
                                 compute='_compute_student_id',
                                 store=True)

    name = fields.Char(related='student_id.name')
    surname = fields.Char(related='student_id.surname')
    phone = fields.Char(related='student_id.phone')
    dob = fields.Date(related='student_id.dob')
    state = fields.Selection(related='student_id.state')
    blood_type = fields.Selection(related='student_id.blood_type')
    subject_id = fields.Many2many(related='student_id.subject_id')
    classroom_id = fields.Many2one(comodel_name='class.rooms',
                                   related='student_id.classroom_id')
    member_type = fields.Selection(related='user_id.member_type')
    sequence = fields.Char(related='student_id.sequence')
    gender = fields.Selection(related='student_id.gender')
    email = fields.Char(related='student_id.email')
    external_email = fields.Char(related='student_id.external_email',
                                 help='Students personal email, not the one that is used to log-in in the system')
    suspend_reason = fields.Text(related='student_id.suspend_reason')
    enrollment_date = fields.Date(related='student_id.enrollment_date')
    graduation_date = fields.Date(related='student_id.graduation_date')
    finance_ids = fields.One2many(related='student_id.finance_ids')
    faculty = fields.Selection(related='student_id.faculty')
    year = fields.Selection(related='student_id.year')
    semester = fields.Selection(related='student_id.semester')
    image_128 = fields.Image(string='Image 128',
                             related='student_id.image_128',
                             tracking=True)

    @api.depends('user_id')
    def _compute_student_id(self):
        """
        Autofill the fields
        """
        logged_user = self.env.user.id
        for rec in self:
            rec.student_id = self.env['students.students'].search([('user_id', '=', logged_user)], limit=1).id

    def action_print_report(self):
        """
        To Generate the report and take the information in a PDF
        """
        self.ensure_one()
        report = self.env['person.profile.information.report']
        pdf_base64 = report.generate_my_profile(self)

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
            'target': 'new',
        }


class StudentSubject(models.Model):
    _name = 'student.subjects'
    _description = 'Student Subjects'

    user_id = fields.Many2one(comodel_name='res.users')
    student_id = fields.Many2one(comodel_name='students.students',
                                 default=lambda self: self.env['students.students'].search(
                                     [('user_id', '=', self.env.user.id)], limit=1))
    subject_id = fields.Many2one(comodel_name='subject.subject')

    student_sequence = fields.Char(string='Student ID', related='student_id.sequence')
    subject_sequence = fields.Char(string='Subject ID', related='subject_id.sequence')

    faculty = fields.Selection(string='Faculty', related='student_id.faculty')
    year = fields.Selection(string='Year', related='student_id.year')
    semester = fields.Selection(string='Semester', related='student_id.semester')

    student_name = fields.Char(string='Student Name', related='student_id.name')
    subject_name = fields.Char(string='Subject Name', related='subject_id.name')

    passed_subject_ids = fields.Many2many('subject.subject', compute='_compute_subject_status', string="Completed")
    upcoming_subject_ids = fields.Many2many('subject.subject', compute='_compute_subject_status', string="Remaining")

    @api.depends('student_id', 'student_id.year', 'student_id.semester')
    def _compute_subject_status(self):
        # Mapping years to numbers for easier comparison
        year_map = {'1st': 1, '2nd': 2, '3rd': 3}

        for rec in self:
            if not rec.student_id:
                rec.passed_subject_ids = False
                rec.upcoming_subject_ids = False
                continue

            # 1. Get all subjects assigned to this student's faculty
            all_curriculum = self.env['subject.subject'].search([('faculty', '=', rec.faculty)])

            # 2. Get Student's Current Level
            current_year_num = year_map.get(rec.year, 0)

            # 3. Filter Passed: Subjects from previous years
            passed = all_curriculum.filtered(lambda s: year_map.get(s.year, 0) < current_year_num)

            # 4. Filter Upcoming: Subjects for current or future years
            upcoming = all_curriculum.filtered(lambda s: year_map.get(s.year, 0) >= current_year_num)

            rec.passed_subject_ids = passed
            rec.upcoming_subject_ids = upcoming
