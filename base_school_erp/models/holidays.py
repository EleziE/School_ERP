from odoo import fields,models

class Holidays(models.Model):
    _name = 'holiday.holiday'
    # _inherit = 'resource.calendar.leaves'

    name = fields.Char(string='Holidays name')
    date = fields.Date(string='Holidays date')

