from odoo import api, fields, models


class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _description = 'Partners'


    book_id = fields.Many2one(string='Book',comodel_name='library.borrow')
