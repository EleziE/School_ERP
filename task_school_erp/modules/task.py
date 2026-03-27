from odoo import fields, models, api


class Task(models.Model):
    _name = 'task'
    _description = 'Task'
    _rec_name = 'created_for'

    created_by = fields.Many2one(comodel_name='teacher.teacher',
                                 string='Created by')
    created_for = fields.Many2one(comodel_name='teacher.teacher',
                                  string="Created for")
    status = fields.Selection(selection=[('new', 'New'),
                                         ('in_progres', 'In Progress'),
                                         ('completed', 'Completed'),
                                         ('completed_delayed', 'Completed / Delayed')],
                              string='Status',
                              default='new',
                              group_expand='_group_expand_status')
    starting_date = fields.Date(string='Starting Date',
                                compute='_compute_starting_date',
                                readonly=True)
    finish_date = fields.Date(string='Finish Date')
    description = fields.Text(string='Description of task')

    def action_new(self):
        self.status = 'new'

    def action_in_progres(self):
        self.status = 'in_progres'

    def action_completed(self):
        self.status = 'completed'

    @api.onchange('starting_date')
    def _compute_starting_date(self):
        self.starting_date = fields.Date.today()

    @api.model
    def _group_expand_status(self, states, domain, order):
        return [key for key, val in self._fields['status'].selection]


class Teacher(models.Model):
    _inherit = 'teacher.teacher'

    task_id = fields.One2many(comodel_name='task', inverse_name='created_for', string='My task', readonly=True)
