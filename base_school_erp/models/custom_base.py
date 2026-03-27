from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResUsersInheritance(models.Model):
    _inherit = 'res.users'

    surname = fields.Char(string='Surname')
    gender = fields.Selection(string='Gender',
                              selection=[('female', 'Female'),
                                         ('male', 'Male')], )
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
    dob = fields.Date(string='Date of birth')
    enrollment_date = fields.Date(string='Enrollment Date',
                                  default=fields.Date.today, )
    member_type = fields.Selection(selection=[('student', 'Student'),
                                              ('teacher', 'Teacher'),
                                              ('administrator', 'Administrator'), ])

    education = fields.Selection(selection=[('bachelor', 'Bachelor'),
                                            ('master', 'Master'),
                                            ('doctorate', 'Doctorate')],
                                 string='Education')
    @api.onchange('name', 'surname')
    def _onchange_name_set_login(self):
        if self.name and self.surname:
            first_initial = self.name.strip()[0].lower()
            surname = self.surname.strip().lower().replace(' ', '')
            self.login = f"{first_initial}.{surname}@school.com"
        elif self.name:
            self.login = False

    @api.constrains('dob')
    def check_dob(self):
        for rec in self:
            today = fields.Date.today()
            if rec.dob and rec.dob > today:
                raise ValidationError("Date of birth  can't be in the future")

