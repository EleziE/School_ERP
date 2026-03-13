from odoo import fields,models

class Task(models.Model):
    _name = 'task'
    _description = 'Task'

    created_by = fields.Many2one(comodel_name='teacher.teacher',string='Created by')
    created_for = fields.Many2one(comodel_name='teacher.teacher',string="Created for")
    status = fields.Selection(selection=[('draft','Draft'),
                                         ('published','Published'),
                                         ('in_progres','In Progress')],
                              string='Status',default='draft')
    starting_date = fields.Date(string='Starting Date')
    finish_date = fields.Date(string='Finish Date')
    description = fields.Text(string='Description of task')

class Teacher(models.Model):
    _inherit = 'teacher.teacher'

    task_id = fields.One2many(comodel_name='task',inverse_name='created_for',string='My task',readonly=True)