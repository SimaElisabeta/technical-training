from odoo import fields, models, api
from odoo.exceptions import ValidationError

class SchoolSchedule(models.Model):
    _name = "school.schedule"
    _description = "School Schedule"

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
        copy=False,
        comodel_name='school.class.location',
        ondelete='restrict',
        domain="[('school_id','=', school_id)]"
    )

    
    class_id = fields.Many2one(
        comodel_name='school.class',
        ondelete='restrict',
        domain="[('school_id','=', school_id)]"
    )

    
    day = fields.Selection(
        copy=False,
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
                raise ValidationError("Start hour must be in between 0-22.")
            if schedule.stop < 1 or schedule.stop > 23:
                raise ValidationError("Stop hour must be in between 1-23.")
            if schedule.stop <= schedule.start:
                raise ValidationError("Stop hour must be greater than Start hour.")
            if (schedule.stop - schedule.start) != 1:
                raise ValidationError("Total time for a course should not exceed 1 hour.")
            
    
    @api.constrains("location_id", "day", "start", "stop")
    def _check_class_available(self):
        for schedule in self:
            conflicting_schedules = self.search([
                ('location_id', '=', schedule.location_id.id),
                ('day', '=', schedule.day),
                ('start', '=', schedule.start),
                ('stop', '=', schedule.stop),
                ('id', '!=', schedule.id),  # Exclude the current record
            ])
            if conflicting_schedules:
                raise ValidationError("Class is not available during this time slot.")
            
    
    @api.constrains("day", "start", "stop", "school_course_teacher_id")
    def _check_teacher_available(self):
        for schedule in self:
            conflicting_schedules = self.search([
                ('day', '=', schedule.day),
                ('start', '=', schedule.start),
                ('stop', '=', schedule.stop),
                ('school_course_teacher_id', '=', schedule.school_course_teacher_id.id),
                ('id', '!=', schedule.id),  # Exclude the current record
            ])
            if conflicting_schedules:
                raise ValidationError("Teacher is already assigned to a course during this time slot.")

    
    def name_get(self):
        result = []
        for schedule in self:
            name = f"{schedule.day.capitalize()} - {schedule.school_course_teacher_id.display_name} - At class: {schedule.class_id.name}"
            result.append((schedule.id, name))
        return result