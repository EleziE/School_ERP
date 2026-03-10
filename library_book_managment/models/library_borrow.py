from odoo import api, fields, models, exceptions


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

    @api.constrains('due_date','borrow_date')
    def _check_due_date(self):
        for rec in self:
            if rec.due_date and rec.borrow_date :
                if rec.due_date < rec.borrow_date:
                    raise exceptions.ValidationError('Due date must be after borrow_date')

    @api.constrains('book_id')
    def _check_available_copies(self):
        for rec in self:
            if rec.book_id and rec.book_id.available_copies ==0 :
                raise exceptions.ValidationError('This book has no available copies')
