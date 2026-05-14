from odoo import fields, models, _, api
from odoo.exceptions import AccessError, ValidationError


class Administration(models.Model):
    _name = 'administration.administration'
    _description = 'Administration'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one(comodel_name='res.users',
                              string='User')
    name = fields.Char(string='Name',
                       tracking=True)
    login = fields.Char(string='Email',
                        related='user_id.login',
                        tracking=True,
                        readonly=False,
                        store=True)
    sequence = fields.Char(string='Administration ID: ',
                           readonly=True,
                           default=lambda self: _('New'))
    surname = fields.Char(string='Surname',
                          tracking=True)
    father_name = fields.Char(string='Father ',
                              tracking=True)
    mother_name = fields.Char(string='Mother ',
                              tracking=True)
    external_email = fields.Char(string='External Email',
                                 tracking=True,
                                 help='Email to communicate with the user, not from the schools email')
    gender = fields.Selection(string='Gender',
                              selection=[('female', 'Female'),
                                         ('male', 'Male')], )
    dob = fields.Date(string='Date of birth',
                      tracking=True)
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
    phone = fields.Char(string='Phone no: ',
                        related='user_id.phone')
    member_type = fields.Selection(related='user_id.member_type',
                                   string='Type')
    image_128=fields.Image(string='Image 128',related='user_id.image_128')

    @api.model_create_multi
    def create(self, vals_list):
        # 1. Fetch references ONCE outside the loop for better performance
        access_rights = self.env.ref('configurations_school_erp.group_school_administration')
        internal_user = self.env.ref('base.group_user')

        for vals in vals_list:
            if vals.get('sequence', _('New')) == _('New'):
                vals['sequence'] = self.env['ir.sequence'].next_by_code('administration.administration')

            user = self.env['res.users'].create({
                'name': vals.get('name'),
                'login': vals.get('login'),
                'member_type': 'administration',
                'groups_id': [
                    (4, access_rights.id),
                    (4, internal_user.id),
                ]
            })

            vals['user_id'] = user.id

        return super(Administration, self).create(vals_list)

    def write(self, vals):

        if not (self.env.user.has_group('configurations_school_erp.group_school_admin')
                or self.env.user.has_group('configurations_school_erp.group_school_administration')):
            raise AccessError('You are do not have the right to modify records')

        secure_fields = {'name', 'login', 'member_type', 'external_email', 'blood_type', 'father_name', 'mother_name',
                         'gender', 'dob', 'phone'}

        return super().write(vals)

    def unlink(self):
        to_be_deleted = self.mapped('user_id')

        result = super(Administration, self).unlink()

        if to_be_deleted:
            to_be_deleted.sudo().unlink()

        return result

    @api.constrains('dob')
    def check_dob(self):
        for rec in self:
            today = fields.Date.today()
            if rec.dob and rec.dob > today:
                raise ValidationError("Date of birth  can't be in the future")
