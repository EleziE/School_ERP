from odoo import fields,models


class Student(models.Model):
    _name = 'students.students'

    user_id = fields.Many2one(comodel_name='res.users')
    name = fields.Char(string='Name',related='user_id.name',readonly=True)
    gender = fields.Selection(string='Gender',selection=[('female','Female'),('male','Male')])
    dob = fields.Date(string='Date of birth')
    blood_type = fields.Char(string='Blood type')
    email = fields.Char(string='Email')
    classroom_id = fields.Many2one(comodel_name='class.rooms',string='Class')
    subject_id = fields.Many2many(comodel_name='subject.subject')

    def action_open_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Assign Classroom',
            'res_model': 'assign.classroom.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_student_ids': [(4, self.id)]
            }
        }

    def action_open_subject_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Assign Subject',
            'res_model': 'assign.subject.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_student_ids': [(4, self.id)]
            }
        }
