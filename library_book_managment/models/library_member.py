from odoo import fields, models,api
from datetime import date

class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'

    partner_id = fields.Many2one(comodel_name='res.partner')
    member_code = fields.Char(string='Member Code',copy=False)
    join_date = fields.Date(string='Joined Date')
    expiry_date = fields.Date(string='Expiry Date')
    is_active = fields.Boolean(string='Active')
    borrow_ids = fields.One2many(string='Borrows',
                                 comodel_name='library.borrow',
                                 inverse_name='member_id')
    borrow_count = fields.Integer(string='Borrow Count',compute='_compute_borrow_count',store=True)
    state = fields.Selection(selection=[
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
    ], string='Status',compute='_compute_state',store=True)

    @api.depends('borrow_ids')
    def _compute_borrow_count(self):
        for rec in self:
            rec.borrow_count = len(rec.borrow_ids)

    @api.depends('expiry_date','is_active')
    def _compute_state(self):
        for rec in self:
            today = fields.Date.today()
            if rec.expiry_date and isinstance(rec.expiry_date, date) < today:
                rec.state = 'expired'
            elif rec.is_active == False:
                rec.state = 'suspended'
            else:
                rec.state = 'active'
    @api.model
    def create(self, vals):
        if not vals.get('member_code'):
            vals['member_code']= self.env['ir.sequence'].next_by_code('library.member')
        return super().create(vals)