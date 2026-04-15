from odoo import fields, models,api,_

class ClassRooms(models.Model):
    _name = 'class.rooms'
    _description = 'Class Room'
    _rec_name = 'name'

    sequence = fields.Char(string='Sequence',readonly=True)
    name = fields.Char(string='Class name')



    @api.model
    def create(self, vals):
        # =================== Per Sequence Generator ====================
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('class.rooms') or _('New')
        # =================== Per Sequence Generator ===================
        return super().create(vals)

    _sql_constraints = [
        ('seq_uq', 'UNIQUE(sequence)', "Sequence already exists !"),
    ]