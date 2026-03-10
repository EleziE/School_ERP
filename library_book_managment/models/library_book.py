from odoo import api, fields, models, exceptions


class LibraryBooks(models.Model):
    _name = 'library.books'
    _description = 'Library Books'

    name = fields.Char(string='Title')
    author_id = fields.Many2one(string='Author',
                                comodel_name='res.partner')
    category_id = fields.Many2one(string='Category',
                                  comodel_name='library.category')
    isbn = fields.Char(string='ISBN')
    total_copies = fields.Integer(string='Copies')
    available_copies = fields.Integer(string='Available Copies',
                                      compute='_compute_available_copies',store=True)
    state = fields.Selection(selection=[('available', 'Available'),
                                        ('partially_available', 'Partially Available'),
                                        ('unavailable', 'Unavailable')],
                             string='State',compute='_compute_copy_state',store=True)
    description = fields.Text(string='Description')
    cover_image = fields.Binary(string='Cover Image')
    publisher = fields.Char(string='Publisher')
    publish_date = fields.Date(string='Publish Date')
    borrow_ids = fields.One2many(string='Borrow',
                                comodel_name='library.borrow',
                                 inverse_name='book_id')
    language = fields.Char(string='Language')
    pages = fields.Integer(string='Pages')






    _sql_constraints = [
        ('unique_isbn','UNIQUE (isbn)','ISBN must be unique'),
    ]

    @api.constrains('total_copies')
    def _total_copies_constraint(self):
        for rec in self:
            if self.total_copies <= 0:
                raise exceptions.ValidationError('Total copies must be positive')



    @api.depends('total_copies', 'borrow_ids')
    def _compute_available_copies(self):
        for rec in self:
            rec.available_copies = rec.total_copies - len(rec.borrow_ids)

    @api.depends('total_copies','available_copies')
    def _compute_copy_state(self):
        for rec in self:
            if rec.available_copies == 0:
                rec.state = 'unavailable'
            elif rec.available_copies == rec.total_copies:
                rec.state = 'available'
            elif rec.available_copies > rec.total_copies or rec.available_copies < rec.total_copies:
                rec.state = 'partially_available'
