from odoo import fields, models

class School(models.Model):
    _name = "school"
    _description = "School App"
    
    name = fields.Char()

    class_ids = fields.One2many(
        comodel_name='school.class',
        inverse_name='school_id',
    )

    class_location_ids = fields.One2many(
        comodel_name='school.class.location',
        inverse_name='school_id',
    )

    school_course_teacher_ids = fields.One2many(
        comodel_name='school.courses.teachers',
        inverse_name='school_id',
    )

    schedule_ids = fields.One2many(
        comodel_name='school.schedule',
        inverse_name='school_id',
    )