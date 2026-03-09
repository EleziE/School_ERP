from odoo import fields,models,api

class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Library Category'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    book_ids = fields.One2many(comodel_name='library.books',
                               inverse_name='category_id',
                               string='Books',store=True)
    book_count = fields.Integer(string='Book Count',compute='_compute_book_count',store=True)


    @api.depends('book_ids')
    def _compute_book_count(self):
        for rec in self:
            rec.book_count = len(rec.book_ids)