from odoo import fields, models, api
from datetime import date, timedelta


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one(comodel_name='res.partner')
    member_code = fields.Char(string='Member Code', copy=False, readonly=True)
    join_date = fields.Date(string='Joined Date', help='Date of joining the library')
    expiry_date = fields.Date(string='Expiry Date', help='Date of expiry if not updated')
    is_active = fields.Boolean(string='Active')
    borrow_ids = fields.One2many(string='Borrows',
                                 comodel_name='library.borrow',
                                 inverse_name='member_id')
    borrow_count = fields.Integer(string='Borrow Count', compute='_compute_borrow_count', store=True)
    state = fields.Selection(selection=[
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
    ], string='Status', compute='_compute_state', store=True)
    phone = fields.Char(string='Phone')

    @api.depends('borrow_ids')
    def _compute_borrow_count(self):
        for rec in self:
            rec.borrow_count = len(rec.borrow_ids)

    @api.depends('expiry_date', 'is_active')
    def _compute_state(self):
        for rec in self:
            today = fields.Date.today()
            if rec.expiry_date and isinstance(rec.expiry_date, date) and rec.expiry_date < today:
                rec.state = 'expired'
            elif not rec.is_active:
                rec.state = 'suspended'
            else:
                rec.state = 'active'

    @api.model
    def create(self, vals):
        if not vals.get('member_code'):
            vals['member_code'] = self.env['ir.sequence'].next_by_code('library.member')
        return super().create(vals)

    _sql_constraints = [
        ('member_code_uniq', 'UNIQUE (member_code)', 'Member code is unique'),
    ]

    @api.onchange('partner_id')
    def _onchange_phone(self):
        if self.partner_id:
            self.phone = self.partner_id.phone
        else:
            self.phone = False

    @api.onchange('join_date')
    def _onchange_expiry_date(self):
        if self.join_date:
            self.expiry_date = self.join_date + timedelta(days=365)