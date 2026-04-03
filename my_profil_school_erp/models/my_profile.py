from odoo import api, fields, models

class Profile(models.Model):
    _name = 'my.profile'

    name = fields.Char(string="Name")

