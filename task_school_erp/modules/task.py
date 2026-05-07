import secrets

from odoo import fields, models, api, _
from odoo.exceptions import UserError, AccessError


class Task(models.Model):
    _name = 'task'
    _description = 'Task'
    _rec_name = 'task_for'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Char(string='Task ID: ',
                           readonly=True,
                           default=lambda self: _('New'))
    user_id = fields.Many2one(comodel_name='res.users',
                              string='User',
                              tracking=True)
    task_for = fields.Many2one(comodel_name='teacher.teacher',
                               tracking=True, )
    task_from = fields.Many2one(comodel_name='administration.administration',
                                readonly=True,
                                default=lambda self: self.env['administration.administration'].search(
                                    [('user_id', '=', self.env.user.id)], limit=1),
                                store=True,
                                tracking=True)
    status = fields.Selection(selection=[('in_progress', 'In Progress'),
                                         ('completed', 'Completed'),
                                         ('completed_delayed', 'Completed / Delayed'),
                                         ('completed_early', 'Completed / Early'), ],
                              compute='status_based_dates',
                              store=True,
                              group_expand='_group_expand_status',
                              tracking=True)
    starting_date = fields.Date(default=fields.Date.today,
                                readonly=True,
                                tracking=True)
    planned_finish_date = fields.Date(tracking=True)
    finish_date = fields.Date(store=True,
                              readonly=True,
                              tracking=True)
    description = fields.Text(tracking=True)
    check_user_finish_date = fields.Boolean(compute='_compute_check_user')
    check_user_planned_finish_date = fields.Boolean(compute='_compute_planed_date_restriction')
    days_report = fields.Integer(string='Days Report',
                                 help='From task to finish time',
                                 compute='_compute_time_between')

    ######################### CREATE & WRITE ################################

    @api.model_create_multi
    def create(self, vals_list):
        # This loop ensures every record in the batch gets a sequence
        for vals in vals_list:
            if vals.get('sequence', _('New')) == _('New'):
                vals['sequence'] = self._generate_unique_sequence()

        # We pass the WHOLE list to super() so the ORM can do a batch insert
        return super().create(vals_list)

    def write(self, vals):
        """
        Who has the rights to modify the records
        """

        is_admin = (self.env.user.has_group('base_school_erp.group_school_administration') or
                    self.env.user.has_group('base_school_erp.group_school_admin') or
                    self.env.user.has_group('base_school_erp.group_school_teacher'))

        if not is_admin:
            raise AccessError('You are not allowed to perform this task!')

        for rec in self:
            was_completed = rec.status in ['completed', 'completed_delayed', 'completed_early']

            if was_completed:

                if 'finish_date' not in vals:
                    raise UserError(
                        '\nThe task has been completed!\n\nYou cannot change the status of the task or modify it !')

        return super().write(vals)

    ######################### Depends ################################

    def action_finish_task(self):
        """The button action. It sets the date, which then triggers the status compute."""
        for rec in self:
            # Check permissions
            if rec.task_for.user_id != self.env.user:
                raise UserError(f'You are not allowed to perform this task, only {rec.task_for.name} is allowed!')

            # Set finish_date to today.
            # Because 'status' depends on 'finish_date', it will update automatically.
            rec.finish_date = fields.Date.today()

    def action_create_task(self):
        for rec in self:
            self.create({})
            if not rec.planned_finish_date:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    "params": {
                        'title': 'Warning',
                        'message': 'The task was created but the planned finish date was left empty!',
                        'type': 'warning',
                        'sticky': False,
                    }
                }
        return None

    @api.depends('planned_finish_date', 'finish_date')
    def status_based_dates(self):
        for rec in self:
            if not rec.finish_date:
                rec.status = 'in_progress'
            elif rec.planned_finish_date:
                if rec.finish_date > rec.planned_finish_date:
                    rec.status = 'completed_delayed'
                elif rec.finish_date < rec.planned_finish_date:
                    rec.status = 'completed_early'
                else:
                    rec.status = 'completed'
            else:
                # If no deadline was set but they finished it
                rec.status = 'completed'

    @api.depends('starting_date', 'planned_finish_date', 'finish_date')
    def _compute_time_between(self):
        for rec in self:
            if rec.finish_date and rec.planned_finish_date:
                diff = (rec.planned_finish_date - rec.finish_date).days
                rec.days_report = diff
            elif not rec.finish_date and rec.planned_finish_date:
                rec.days_report = (rec.planned_finish_date - fields.Date.today()).days
            else:
                rec.days_report = 0

    def _generate_unique_sequence(self):
        while True:
            number = str(secrets.randbelow(9000000) + 1000000)
            sequence = f'TSK-{number}'
            existing = self.search([('sequence', '=', sequence)], limit=1)
            if not existing:
                return sequence

    ######################### Constraints ################################
    @api.constrains('finish_date')
    def check_user(self):
        """
        Constraint that prevent anyone to enter the finish date except the person who the task is for
        """
        for rec in self:
            if rec.finish_date:
                if rec.task_for.user_id != self.env.user:
                    raise UserError(
                        f'You are not allowed to perform this task, only {rec.task_for.name} is allowed to !')

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

    _sql_constraints = [
        ('seq_uq', 'UNIQUE(sequence)', "Sequence already exists !"),
    ]

    ######################### Recheck for the fields  ################################

    @api.depends('task_for')
    def _compute_check_user(self):
        for rec in self:
            rec.check_user_finish_date = (rec.task_for.user_id == self.env.user)

    @api.depends('task_from')
    def _compute_planed_date_restriction(self):
        for rec in self:
            rec.check_user_planned_finish_date = (rec.task_from.user_id == self.env.user)

    ######################### Dont understand what they do yet  ################################

    def _group_expand_status(self, states, domain, order):
        return [key for key, val in self._fields['status'].selection]


class Teacher(models.Model):
    _inherit = 'teacher.teacher'

    task_id = fields.One2many(comodel_name='task',
                              inverse_name='task_for',
                              string='My task')
