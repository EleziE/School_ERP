from odoo import fields, models, api


class Teacher(models.Model):
    _name = 'teacher.teacher'


    user_id = fields.Many2one(comodel_name='res.users', required=True)
    name = fields.Char(string='Name', related="user_id.name", readonly=True)
    phone = fields.Char(string='Phone', related="user_id.phone", readonly=True)
    mobile = fields.Char(string='Mobile', related="user_id.mobile", readonly=True)
    dob = fields.Date(string='Date of birth', related="user_id.dob", readonly=True)

    subject_id = fields.Many2many(comodel_name='subject.subject')
    class_room_id = fields.Many2many(comodel_name='class.rooms')

    _sql_constraints = [
        ('user_id', 'UNIQUE(user_id)', 'The name must be unique'), ]

    def action_open_subject_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Assign Subject',
            'res_model': 'subject.teacher.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teacher_id': self.id  # ← pre-fills current teacher
            }
        }


class Student(models.Model):
    _inherit = 'students.students'

    teacher_id = fields.Many2many(comodel_name='teacher.teacher',
                                  relation='teacher_student',
                                  column1='student',
                                  column2='teacher',
                                  compute='_compute_teacher',
                                  readonly=True)

    @api.onchange('classroom_id')
    def _compute_teacher(self):
        teachers = self.env['teacher.teacher'].search([('class_room_id', 'in', self.classroom_id.id)])
        self.teacher_id = teachers


class ResUser(models.Model):
    _inherit = 'res.users'

    dob = fields.Date(string='Date of birth')

    education = fields.Selection(selection=[('bachelor', 'Bachelor'),
                                            ('master', 'Master'),
                                            ('doctorate', 'Doctorate')],
                                 string='Education')
