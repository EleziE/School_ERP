from odoo import fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    library_card_number = fields.Char(string='Library Card Number')
    books_borrowed = fields.Integer(string='Books Borrowed')