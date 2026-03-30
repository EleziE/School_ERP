from odoo import  fields, models

class Administration(models.Model):
    _name = 'administration.administration'
    _description = 'Administration'

    user_id = fields.Many2one(comodel_name='res.users',string='User')
    name = fields.Char(string='Name',related='user_id.name')
    email = fields.Char(string='Email',related='user_id.email')

