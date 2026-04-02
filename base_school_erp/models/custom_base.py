from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResUsersInheritance(models.Model):
    _inherit = 'res.users'

    member_type = fields.Selection(selection=[('none', 'None'),
                                              ('student', 'Student'),
                                              ('teacher', 'Teacher'),
                                              ('administrator', 'Administrator'), ],
                                   store=True)





