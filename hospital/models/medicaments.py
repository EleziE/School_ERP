from odoo import fields,models


class Medicaments(models.Model):
    _name = 'hospital.medicaments'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Medicament',tracking=True)
    manufacturer = fields.Date(string='Manufacturer Date',tracking=True)
    expiration_date = fields.Date(string='Expiration Date',tracking=True)
    number = fields.Char(string='Quantity',tracking=True)


