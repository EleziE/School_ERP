from odoo import fields, models, api


class HospitalPerson(models.Model):
    _name = 'hospital.person'
    _inherit = ['mail.thread','mail.activity.mixin']


    name = fields.Char(string='Name',tracking=True)
    surname = fields.Char(string='Surname',tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender',tracking=True)
    dob = fields.Date(string='Date of Birth',tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age')



    # Calculation of the age (not stored)
    @api.depends('dob')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.dob:
                years = today.year - record.dob.year
                if (today.month, today.day) < (record.dob.month, record.dob.day):
                    years -= 1
                record.age = years
            else:
                record.age = 0


class HospitalDoctors(models.Model):
    _name = 'hospital.doctors'
    _inherit = 'hospital.person'

    specialisation = fields.Selection(string='Specialisation', selection=[
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('endocrinology', 'Endocrinology'),
        ('gastroenterology', 'Gastroenterology'),
        ('geriatrics', 'Geriatrics'),
        ('gynecology', 'Gynecology'),
        ('hematology', 'Hematology'),
        ('internal_medicine', 'Internal Medicine'),
        ('nephrology', 'Nephrology'),
        ('neurology', 'Neurology'),
        ('obstetrics', 'Obstetrics'),
        ('oncology', 'Oncology'),
        ('ophthalmology', 'Ophthalmology'),
        ('orthopedics', 'Orthopedics'),
        ('otorhinolaryngology', 'Otorhinolaryngology (ENT)'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('pulmonology', 'Pulmonology'),
        ('radiology', 'Radiology'),
        ('rheumatology', 'Rheumatology'),
        ('surgery_general', 'General Surgery'),
        ('urology', 'Urology'),
    ])
    patient_id = fields.One2many(comodel_name='hospital.patient',
                                 inverse_name='doctor_id',
                                 string="Patient's")

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit='hospital.person'

    doctor_id = fields.Many2one(comodel_name='hospital.doctors',
                                string='Doctor')

    medicaments_ids = fields.Many2many(comodel_name='hospital.medicaments',
                                       column1='patients_id',
                                       column2='medicament_id',
                                       string='Medicaments',
                                       relation='medicament_patient_rel',
                                       tracking=True)

    prescription = fields.Html(string='Prescription')