from odoo import fields, models


class Subject(models.Model):
    _name = 'subject.subject'

    name = fields.Char(string='Subject name')
    credits = fields.Integer(string='Credits')










class ClassRooms(models.Model):
    _name = 'class.rooms'

    name = fields.Char(string='Class name')