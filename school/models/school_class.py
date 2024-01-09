from odoo import fields, models

class SchoolClass(models.Model):
    _name = "school.class"
    _description = "School Class"
    
    name = fields.Char()

    school_id = fields.Many2one(
        comodel_name='school',
        ondelete='restrict',
    )

    # DIRIGINTE
    teacher_id = fields.Many2one(
        string='Class Master',
        comodel_name='res.partner',
        ondelete='restrict',
        domain=[('is_teacher','=',True)]
    )

    student_ids = fields.One2many(
        comodel_name='res.partner',
        inverse_name='class_id',
    )
    
    