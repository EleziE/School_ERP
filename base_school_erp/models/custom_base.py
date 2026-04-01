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
    member_type = fields.Selection(selection=[('none', 'None'),
                                              ('student', 'Student'),
                                              ('teacher', 'Teacher'),
                                              ('administrator', 'Administrator'), ],
                                   store=True)

    education = fields.Selection(selection=[('bachelor', 'Bachelor'),
                                            ('master', 'Master'),
                                            ('doctorate', 'Doctorate')],
                                 string='Education')

    @api.onchange('name', 'surname', 'member_type')
    def _onchange_name_set_login(self):
        if not self.name or not self.surname:
            self.login = False
            return

        first_initial = self.name.strip()[0].lower()
        surname = self.surname.strip().lower().replace(' ', '')
        domains = {
            'student': 'std.school.edu.com',
            'teacher': 'tec.school.edu.com',
            'administrator': 'adm.school.edu.com'
        }

        domain = domains.get(self.member_type)
        if domain:
            self.login = f"{first_initial}.{surname}@{domain}"
        else:
            self.login = False

    @api.constrains('dob')
    def check_dob(self):
        for rec in self:
            today = fields.Date.today()
            if rec.dob and rec.dob > today:
                raise ValidationError("Date of birth  can't be in the future")

    @api.model_create_multi
    def create(self, vals_list):
        domains = {
            'student': 'std.school.edu.com',
            'teacher': 'tec.school.edu.com',
            'administrator': 'adm.school.edu.com'
        }
        for vals in vals_list:
            name = vals.get('name', '')
            surname = vals.get('surname', '')
            member_type = vals.get('member_type', '')
            domain = domains.get(member_type)
            if name and surname and domain:
                first_initial = name.strip()[0].lower()
                surname_clean = surname.strip().lower().replace(' ', '')
                vals['login'] = f"{first_initial}.{surname_clean}@{domain}"
        return super().create(vals_list)




