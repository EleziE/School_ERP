from odoo import api, fields, models


class MyProfileAdministration(models.Model):
    _name = 'my.profile.administration'
    _description = 'My Profile Administration'

    user_id = fields.Many2one(comodel_name='res.users')
    administration_id = fields.Many2one(comodel_name='administration.administration',compute='_compute_info',store=True)


    name = fields.Char(related='administration_id.name')
    surname = fields.Char(related='administration_id.surname')
    father_name = fields.Char(related='administration_id.father_name')
    mother_name = fields.Char(related='administration_id.mother_name')
    external_email =fields.Char(related='administration_id.external_email')
    email = fields.Char(related='administration_id.login')
    gender = fields.Selection(related='administration_id.gender')
    dob = fields.Date(related='administration_id.dob')
    blood_type = fields.Selection(related='administration_id.blood_type')
    phone = fields.Char(related='administration_id.phone')
    member_type = fields.Selection(related='administration_id.member_type')

    @api.depends('user_id')
    def _compute_info(self):

        logged = self.env.user.id
        for rec in self:
            rec.administration_id = rec.env['administration.administration'].search([('user_id', '=', logged)], limit=1)

