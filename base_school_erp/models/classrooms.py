from odoo import fields, models

class ClassRooms(models.Model):
    _name = 'class.rooms'
    _description = 'Class Room'
    _rec_name = 'name'

    name = fields.Char(string='Class name')
