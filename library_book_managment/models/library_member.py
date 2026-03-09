from odoo import fields, models


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'


    partner_id = fields.Many2one('res.partner')
    member_code = fields.Char(string='Member Code')
    join_date = fields.Datetime(string='Joined Date')
    expiry_date = fields.Datetime(string='Expiry Date')
    is_active = fields.Boolean(string='Active')
    borrow_ids = fields.One2many(string='Borrows',comodel_name='library.member',inverse_name='partner_id')
    borrow_count = fields.Integer(string='Borrow Count')
    state = fields.Selection(selection=[
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
    ],string='Status')
