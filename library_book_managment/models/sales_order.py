from odoo import fields,models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    library_reference = fields.Char(string='Reference References')