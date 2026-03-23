from odoo import fields,models,api,exceptions


class Exams(models.Model):
    _name = 'exams'
    _description = 'Exams'

    name = fields.Char(string='Exam')
    date_of_exam = fields.Date(string='Date of exam')

    @api.constrains('date_of_exam')
    def _check_exam_holiday(self):
        for rec in self:
            holiday = self.env['holiday.holiday'].search([
                ('date', '=', rec.date_of_exam)
            ])
            if holiday:
                raise exceptions.ValidationError("Exam day is a holiday, it can't be scheduled.")
