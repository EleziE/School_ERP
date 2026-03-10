from odoo import api, fields, models


class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _description = 'Library Borrow'

    book_id = fields.Many2one(string='Book', comodel_name='library.books')
    member_id = fields.Many2one(comodel_name='library.member', string='Member')
    state = fields.Selection([('draft', 'Draft'),
                              ('borrowed', 'Borrowed'),
                              ('returned', 'Returned')],
                             string='State',default='draft')
    borrow_date = fields.Date(string='Borrow Date')
    due_date = fields.Date(string='Due Date')
    return_date = fields.Date(string='Return Date')
    notes = fields.Text(string='Notes')


    def action_borrow(self):
        self.state = 'borrowed'

    def action_return(self):
        self.state = 'returned'
        self.return_date = fields.Date.today()

    def action_reset(self):
        self.state = 'draft'