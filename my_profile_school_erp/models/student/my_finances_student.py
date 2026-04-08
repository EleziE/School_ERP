from odoo import api, fields, models


class MyFinances(models.Model):
    _name = 'my.finances.student'

    student_id = fields.Many2one(comodel_name='students.students')
    created_by = fields.Many2one(comodel_name='finance.finance')
    created_by_info = fields.Char(related='created_by.created_by_info')
    amount = fields.Float(related='created_by.amount')
    reason = fields.Char(related='created_by.reason')
    state = fields.Selection(related='created_by.state')

    def my_finance_student(self):
        """
            Don't know what is the difference between the args 'student_id' and without it since i don't know what th def does hy hy hy
            Does the def need an api.depend or something function to work since like this is just unused as a button waiting to be called
            """
        user = self.env.user.id
        # records = self.search([('created_by', '=', user)]) NOT NEEDED DOMAIN DOES ITS JOB !!! (in this case)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'finance.finance',
            'view_mode': 'tree,form',
            'domain': [('created_by', '=', user)],
            'name': 'My Finances',
        }

    @api.onchange('student_id')
    def _compute_student_id(self):
        logged_user = self.env.user.id
        for rec in self:
            rec.student_id = self.env['finance.finance'].search([('student_id', '=', logged_user)], limit=1).id
