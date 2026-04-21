from odoo import  fields, models,_,api

class Administration(models.Model):
    _name = 'administration.administration'
    _description = 'Administration'
    _inherit = ['mail.thread','mail.activity.mixin']

    user_id = fields.Many2one(comodel_name='res.users',string='User')
    name = fields.Char(string='Name',
                       store=True, tracking=True)
    login = fields.Char(string='Email',related='user_id.login',readonly=False)
    sequence = fields.Char(string='Administration ID: ',
                           readonly=True,
                           default=lambda self: _('New'))
    surname = fields.Char(string='Surname',tracking=True)
    father_name = fields.Char(string='Father ',tracking=True)
    mother_name = fields.Char(string='Mother ',tracking=True)
    external_email = fields.Char(string='External Email',help='Email to communicate with the user, not from the schools email')
    gender = fields.Selection(string='Gender',
                              selection=[('female', 'Female'),
                                         ('male', 'Male')], )
    dob = fields.Date(string='Date of birth',tracking=True)
    blood_type = fields.Selection(selection=[('a+', 'A+'),
                                             ('a-', 'A-'),
                                             ('b+', 'B+'),
                                             ('b-', 'B-'),
                                             ('ab+', 'AB+'),
                                             ('ab-', 'AB-'),
                                             ('o+', 'O+'),
                                             ('o-', 'O-'),
                                             ],
                                  string='Blood Type')
    phone = fields.Char(string='Phone no ',
                        related='user_id.phone',
                        placeholder="+355XX XXX XXXX")
    member_type = fields.Selection(related='user_id.member_type',
                                   string='Type',
                                   readonly=True, )


    @api.model
    def create(self, vals):
    # =================== For Sequence Generator ====================
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('administration.administration')

    # =================== For Access Rights Generator ===================
        access_rights = self.env.ref('base_school_erp.group_school_administration')
        internal_user = self.env.ref('base.group_user')

        user = self.env['res.users'].create({
            'name': vals.get('name'),
            'login': vals.get('login'),
            'member_type': 'administration',
            'groups_id': [
                (4, access_rights.id),
                (4, internal_user.id), ]
        })
        vals['user_id'] = user.id
        print('A administration worker was created')

        return super().create(vals)