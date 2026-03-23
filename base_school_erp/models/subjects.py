from odoo import fields, models


class Subject(models.Model):
    _name = 'subject.subject'
    _description = 'Subject'

    name = fields.Char(string='Subject name')
    credits = fields.Integer(string='Credits')