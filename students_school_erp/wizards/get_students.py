from odoo import fields, models

class Get_Students(models.TransientModel):
    _name = 'get.students'

    student_id = fields.Many2one(comodel_name='students.students')
    dob = fields.Date(related='student_id.dob')

# Still not working ofc is not made yet