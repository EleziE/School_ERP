from odoo import fields,models

class Holidays(models.Model):
    _name = 'holiday.holiday'

    name = fields.Char(string='Holidays name')
    date = fields.Date(string='Holidays date')

