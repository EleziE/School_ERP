from odoo import fields, models


class ResUsersInheritance(models.Model):
    _inherit = 'res.users'

    member_type = fields.Selection(selection=[('none', 'None'),
                                              ('student', 'Student'),
                                              ('teacher', 'Teacher'),
                                              ('administration', 'Administration'),
                                              ('admin', 'Admin'), ],
                                   store=True)
