from odoo import fields, models

class SchoolCourses(models.Model):
    _name = "school.courses"
    _description = "School Courses"

    name = fields.Char()

    
    courses_ids = fields.One2many(
        comodel_name='school.courses.teachers',
        inverse_name='course_id',
    )


class SchoolCoursesTeachers(models.Model):
    _name = "school.courses.teachers"
    _description = "School Courses Teacher"

    school_id = fields.Many2one(
        comodel_name='school',
        ondelete='restrict',
    )

    teacher_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete='restrict',
        domain=[('is_teacher','=',True)]
    )

    course_id = fields.Many2one(
        comodel_name='school.courses',
        ondelete='restrict',
    )
   