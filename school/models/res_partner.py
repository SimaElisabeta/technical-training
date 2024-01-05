from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"
    
    is_teacher = fields.Boolean()
    is_parent = fields.Boolean()
    is_student = fields.Boolean()
    
    
    class_id = fields.Many2one(
        comodel_name='school.class',
        ondelete='restrict',
    )
    
    school_course_teacher_ids = fields.One2many(
        comodel_name='school.courses.teachers',
        inverse_name='teacher_id',
    )
    