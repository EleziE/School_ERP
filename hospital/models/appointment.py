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
                    raise ValidationError("Appointment Date can't be in the past")

    def action_test(self):
        print('test')