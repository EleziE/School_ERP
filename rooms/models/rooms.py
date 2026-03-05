from odoo import fields, models


class Rooms(models.Model):
    _name = 'rooms.rooms'
    _description = 'Rooms'

    name = fields.Char()
