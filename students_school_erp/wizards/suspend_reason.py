from odoo import fields, models, api


class SuspendReason(models.TransientModel):
    _name = 'suspend_reason_wizard'
    _description = 'Suspend Student Wizard'

    student_id = fields.Many2one(
        comodel_name='students.students',
        string='Student',
        readonly=True
    )
    reason = fields.Text(string='Suspension Reason', required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['student_id'] = self.env.context.get('active_id')
        return res

    def action_confirm_suspend(self):
        self.student_id.sudo().write({
            'state': 'inactive',
            'suspend_reason': self.reason,
        })