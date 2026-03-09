import datetime

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Appointments(models.Model):
    _name = 'hospital.appointments'
    _description = 'Appointments'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'patient_id'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string='Patient')
    doctor_id = fields.Many2one(comodel_name='hospital.doctors', string='Doctor')
    appointment_date = fields.Datetime(string='Appointment Date')
    appointment_time = fields.Char(string='Appointment Time', compute='_compute_appointment_time')

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")

    state = fields.Selection([
        ('personal_info', 'Personal Info'),
        ('date_time', 'Date & Time'),
        ('recheck', 'Recheck'),
        ('done', 'Done'),
        ('submit', 'Submit')], string="State", default='personal_info', required=True)

    def action_go_to_date_time(self):
        for rec in self:
            if not rec.name:
                raise ValidationError("Please fill in the First Name before proceeding!")
            if not rec.surname:
                raise ValidationError("Please fill in the Last Name before proceeding!")
            if not rec.dob:
                raise ValidationError("Please fill in the Date of Birth before proceeding!")
            rec.state = 'date_time'

    def action_go_to_recheck(self):
        for rec in self:
            if not rec.appointment_date:
                raise ValidationError("Please fill in the Appointment Date before proceeding!")
            rec.state = 'recheck'

    def action_go_to_done(self):
        for rec in self:
            rec.state = 'done'

    def action_go_back(self):
        for rec in self:
            if rec.state == 'date_time':
                rec.state = 'personal_info'
            elif rec.state == 'recheck':
                rec.state = 'date_time'
            elif rec.state == 'done':
                rec.state = 'recheck'

    @api.depends('appointment_date')
    # From the appointment_date gets only the time
    def _compute_appointment_time(self):
        for rec in self:
            if rec.appointment_date:

                user_datetime = fields.Datetime.context_timestamp(self, rec.appointment_date)
                rec.appointment_time = user_datetime.strftime('%H:%M')
            else:
                rec.appointment_time = ''

    @api.constrains('appointment_date')
    # Appointment date cant be in the past
    def _check_appointment_date(self):
        for rec in self:
            today = datetime.date.today()
            if rec.appointment_date:
                appointment_date = rec.appointment_date.date()
                if appointment_date < today:
                    raise ValidationError("Appointment date can't be in the past")

    def action_test(self):
        print('test')
