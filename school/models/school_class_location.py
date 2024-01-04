from odoo import fields, models

class SchoolClassLocation(models.Model):
    _name = "school.class.location"
    _description = "School Class Location"
    
    name = fields.Char()
    
    school_id = fields.Many2one(
        comodel_name='school',
        ondelete='restrict',
    )
    