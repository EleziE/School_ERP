from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = 'students.students'
    _description = 'Students'
    _inherit=['mail.thread','mail.activity.mixin']

    # Dont know how i did it (learn python baboo se ske gja per terezi )
    sequence = fields.Char(string='Student ID: ',
                           readonly=True,
                           default=lambda self: _('New'))

    user_id = fields.Many2one(comodel_name='res.users',
                              invisible=True, )
    name = fields.Char(string='Name',
                       store=True,tracking=True)
    surname = fields.Char(string='Surname',tracking=True)
    father_name = fields.Char(string='Father ',tracking=True)
    mother_name = fields.Char(string='Mother ',tracking=True)
    # Pse duhet me e ba ti readonly=False , kur ti se ke ba kun readonly=True (ose kshu ma ban te CP)
    email = fields.Char(string='Email',
                        related='user_id.login',
                        readonly=False,tracking=True)
    external_email = fields.Char(string='External Email',help='Email to communicate with the user, not from the schools email')
    gender = fields.Selection(string='Gender',
                              selection=[('female', 'Female'),
                                         ('male', 'Male')], )
    dob = fields.Date(string='Date of birth',tracking=True)
    blood_type = fields.Selection(selection=[('a+', 'A+'),
                                             ('a-', 'A-'),
                                             ('b+', 'B+'),
                                             ('b-', 'B-'),
                                             ('ab+', 'AB+'),
                                             ('ab-', 'AB-'),
                                             ('o+', 'O+'),
                                             ('o-', 'O-'),
                                             ],
                                  string='Blood Type')
    classroom_id = fields.Many2one(comodel_name='class.rooms',
                                   string='Class')
    subject_id = fields.Many2many(comodel_name='subject.subject')
    state = fields.Selection(selection=[('new', 'New'),
                                        ('active', 'Active'),
                                        ('inactive', 'Not Active'),
                                        ('suspended', 'Suspended'),
                                        ('graduated', 'Graduated'),
                                        ('rejected', 'Rejected'), ],
                             string='State',
                             default='new',tracking=True)
    suspend_reason = fields.Text(string='Suspension Reason',tracking=True)
    phone = fields.Char(string='Phone no ',
                        related='user_id.phone',
                        placeholder="+355XX XXX XXXX")
    enrollment_date = fields.Date(string='Enrollment Date',
                                  default=fields.Date.today, )
    graduation_date = fields.Date(string='Graduation Date',
                                  store=True,
                                  readonly=True,
                                  compute='_compute_graduation_date', )
    member_type = fields.Selection(related='user_id.member_type',
                                   string='Type',
                                   readonly=True, )
    user_password = fields.Char(string='Password',
                                related='user_id.new_password', )
    birthday_certificate = fields.Binary(string='Birthday Certificate')
    birthday_certificate_name = fields.Char(string='File name',
                                            default="Document",
                                            accept="application/pdf,"
                                                   "image/png,"
                                                   "image/jpeg")
    year = fields.Selection(string='Year',related='subject_id.year',readonly=False,store=True)
    faculty = fields.Selection(string='Faculty',related='subject_id.faculty',readonly=False,store=True)

    @api.model
    def create(self, vals):
        # =================== Per Sequence Generator ====================
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('students.students') or _('New')
        # =================== Per Sequence Generator ===================

        # =================== Per Access Rights Generator ===================
        access_rights = self.env.ref('base_school_erp.group_school_student')
        internal_user = self.env.ref('base.group_user')

        user = self.env['res.users'].create({
            'name': vals.get('name'),
            'login': vals.get('email'),
            'member_type': 'student',
            'groups_id': [
                (4, access_rights.id),
                (4, internal_user.id), ]
        })
        vals['user_id'] = user.id
        print('A student was created')
        # =================== Per Access Rights Generator ===================

        return super().create(vals)

    def action_print_report(self):
        """Button action to generate PDF"""
        self.ensure_one()  # only one student at a time
        pdf_file = self.env['report.students_module.student_report_pdf'].generate_pdf(self)

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=students.students&id=%s&field=birthday_certificate&download=true' % self.id,
            'target': 'new',
        }

    @api.constrains('user_id')
    def _check_user_not_teacher(self):
        for rec in self:
            if rec.user_id and rec.user_id.member_type == 'teacher':
                raise ValidationError(
                    f"'{rec.user_id.name}' is already a Teacher and cannot be a Student."
                )

    @api.constrains('dob')
    def check_dob(self):
        for rec in self:
            today = fields.Date.today()
            if rec.dob and rec.dob > today:
                raise ValidationError("Date of birth  can't be in the future")

    def action_open_suspend_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Suspend Student',
            'res_model': 'suspend_reason_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

    @api.depends('state')
    def _compute_graduation_date(self):
        for rec in self:
            if rec.state == 'graduated':
                rec.graduation_date = fields.Date.today()
            else:
                rec.graduation_date = False

    # TO-DO Recheck it (understand it)
    # Open My profile with right records
    # def action_open_my_profile(self):
    #     student = self.search([('user_id', '=', self.env.uid)], limit=1)
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'My Profile',
    #         'res_model': 'students.students',
    #         'view_mode': 'form',
    #         'res_id': student.id,
    #         'views': [(self.env.ref('students_school_erp.my_profile_student').id, 'form')],
    #         'target': 'current',
    #     }
    ############################ Buttons ###########################################

    def action_graduated(self):
        self.state = 'graduated'

    def action_active(self):
        self.state = 'active'

    def action_inactive(self):
        self.state = 'inactive'

    ############################ Constraints ############################
    _sql_constraints = [
        ('unique_student_id', 'UNIQUE (sequence)', 'This Student ID already exists.'),
        ('unique_user_id', 'UNIQUE (user_id)', 'This User ID already exists.'),
        ('dob_check', 'CHECK(dob < CURRENT_DATE)', 'Date of birth must be in the past.')
    ]
