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
                                         ('in_progress', 'In Progress'),
                                         ('completed', 'Completed'),
                                         ('completed_delayed', 'Completed / Delayed'),
                                         ('completed_early', 'Completed Early'),
                                         ],
                              compute='status_based_dates',
                              store=True,
                              group_expand='_group_expand_status')
    starting_date = fields.Date(
        default=fields.Date.today,
        readonly=True)
    planned_finish_date = fields.Date()
    finish_date = fields.Date(store=True)
    description = fields.Text()

    def action_in_progres(self):
        self.status = 'in_progress'

    def action_completed(self):
        self.status = 'completed'

    def _group_expand_status(self, states, domain, order):
        return [key for key, val in self._fields['status'].selection]

    @api.depends('planned_finish_date', 'finish_date')
    def status_based_dates(self):
        for rec in self:
            if not rec.planned_finish_date or not rec.finish_date:
                rec.status = 'in_progress'
            elif rec.finish_date == rec.planned_finish_date:
                rec.status = 'completed'
            elif rec.finish_date > rec.planned_finish_date:
                rec.status = 'completed_delayed'
            else:
                rec.status = 'completed_early'


class Teacher(models.Model):
    _inherit = 'teacher.teacher'

    task_id = fields.One2many(comodel_name='task', inverse_name='created_for', string='My task', readonly=True)
