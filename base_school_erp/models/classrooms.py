from odoo import fields, models

class ClassRooms(models.Model):
    _name = 'class.rooms'

    name = fields.Char(string='Class name')