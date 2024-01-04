from odoo import fields, models

class School(models.Model):
    _name = "school"
    _description = "School App"
    
    name = fields.Char()
    