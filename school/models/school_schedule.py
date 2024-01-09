from odoo import fields, models, api
from odoo.exceptions import ValidationError

class SchoolSchedule(models.Model):
    _name = "school.schedule"
    _description = "School Schedule"

    display_name = fields.Char(compute='_compute_display_name', string="Schedule Name")

    school_course_teacher_id = fields.Many2one(
        comodel_name='school.courses.teachers',
        ondelete='restrict',
    )

    school_id = fields.Many2one(
        related="school_course_teacher_id.school_id",
        store=True
    )
    teacher_id = fields.Many2one(
        related="school_course_teacher_id.teacher_id",
        store=True
    )
    course_id = fields.Many2one(
       related="school_course_teacher_id.course_id",
        store=True
    )


    location_id = fields.Many2one(
        comodel_name='school.class.location',
        ondelete='restrict',
        domain="[('school_id','=', school_id)]"
    )

    
    day = fields.Selection(
        selection=[
            ('mon', 'Monday'), 
            ('tue', 'Tuesday'),
            ('wed', 'Wednesday'),
            ('thu', 'Thursday'),
            ('fri', 'Friday'),
            ]
    )

    
    start = fields.Integer()
    stop = fields.Integer()

    
    @api.constrains("start", "stop")
    def _check_start_stop(self):
        for schedule in self:
            if schedule.start < 0 or schedule.start > 22:
                raise ValidationError("Start hour must be in between 0-22")
            if schedule.stop < 1 or schedule.stop > 23:
                raise ValidationError("Stop hour must be in between 1-23")
            if schedule.stop <= schedule.start:
                raise ValidationError("Stop hour must be greater than Start hour")

    
    @api.depends('day', 'school_course_teacher_id')
    def _compute_display_name(self):
        for record in self:
            combined_name = f"{record.day} -> {record.school_course_teacher_id.display_name}"
            record.display_name = '' if 'False' in combined_name else combined_name