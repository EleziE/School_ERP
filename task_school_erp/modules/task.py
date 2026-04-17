from odoo import fields, models, api, _
from odoo.exceptions import UserError


class Task(models.Model):
    _name = 'task'
    _description = 'Task'
    _rec_name = 'created_for'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Char(string='Task ID: ',
                           readonly=True,
                           default=lambda self: _('New'))

    # TO-DO  check in Readme "To Do #1"
    created_by = fields.Many2one(comodel_name='teacher.teacher',
                                 string='Created by',
                                 default=lambda self: self.env['teacher.teacher'].search(
                                     [('user_id', '=', self.env.uid)], limit=1),
                                 readonly=True)

    teacher_id = fields.Many2one(comodel_name='teacher.teacher', )

    created_for = fields.Many2one(comodel_name='teacher.teacher',
                                  string="Created for",
                                  help='Tasks are created only for teachers',tracking=True )

    status = fields.Selection(selection=[('new', 'New'),
                                         ('in_progress', 'In Progress'),
                                         ('completed', 'Completed'),
                                         ('completed_delayed', 'Completed / Delayed'),
                                         ('completed_early', 'Completed Early'), ],
                              compute='status_based_dates',
                              store=True,
                              group_expand='_group_expand_status',tracking=True)

    starting_date = fields.Date(default=fields.Date.today)

    planned_finish_date = fields.Date()

    finish_date = fields.Date(store=True)

    description = fields.Text()

    check_user_finish_date = fields.Boolean(compute='_compute_check_user')

    @api.model
    def create(self, vals):
        # =================== Per Sequence Generator ====================
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('task')
        return super().create(vals)
        # =================== Per Sequence Generator ===================

    @api.depends('created_for')
    def _compute_check_user(self):
        for rec in self:
            rec.check_user_finish_date = (rec.created_for.user_id == self.env.user)

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
    ######################### Constraints ################################
    @api.constrains('finish_date')
    def check_user(self):
        """
        Constraint that prevent anyone to enter the finish date except the person who the task is for
        """
        for rec in self:
            if rec.finish_date:
                if rec.created_for.user_id != self.env.user:
                    raise UserError(
                        f'You are not allowed to perform this task, only {rec.created_for.name} is allowed to !')

    @api.constrains('status')
    def status_lock(self):
        """
        After setting this to one of the statuses it cannot be changed anymore!
        """
        for rec in self:
            if rec._origin.status in ['completed', 'completed_delayed', 'completed_early']:
                if rec._origin.finish_date != rec.finish_date:
                    raise UserError(
                        'This task is already completed. If you need modifications please contact the administrator to make changes.')

    @api.constrains('planned_finish_date', 'finish_date')
    def restriction_date(self):
        for rec in self:
            if rec.planned_finish_date and rec.planned_finish_date < rec.starting_date:
                raise UserError('The planned finish date cannot be in the past!')
            if rec.finish_date and rec.finish_date < rec.starting_date:
                raise UserError('The finish date cannot be before the starting date!')
            """
            Why it cant be :
            ```
            @api.constrains('planned_finish_date', 'finish_date')
            def restriction_date(self):
            for rec in self:
                if rec.planned_finish_date or rec.finish_date < rec.starting_date:
                    raise UserError('The task cant be arranged for the past, it should be in the future')
            
            """

    _sql_constraints = [
        ('seq_uq', 'UNIQUE(sequence)', "Sequence already exists !"),
    ]
    ######################### Constraints ################################

class Teacher(models.Model):
    _inherit = 'teacher.teacher'

    task_id = fields.One2many(comodel_name='task', inverse_name='created_for', string='My task', readonly=True)
