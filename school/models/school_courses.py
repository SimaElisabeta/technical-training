from odoo import fields, models, api

# defines what courses exists universally
class SchoolCourses(models.Model):
    _name = "school.courses"
    _description = "School Courses"

    # the name of the course (eg. English, Math)
    name = fields.Char()

    # one course can be taught by several teachers
    # record of courses 
    courses_ids = fields.One2many(
        comodel_name='school.courses.teachers',
        inverse_name='course_id',
    )

# CoursesTeachers = role (eg. math teacher, english teacher)
class SchoolCoursesTeachers(models.Model):
    _name = "school.courses.teachers"
    _description = "School Courses Teacher"

    # human readable name displayed in UI
    display_name = fields.Char(compute='_compute_display_name', string="Course Name")

    # multiple teacher roles can belong to one school
    school_id = fields.Many2one(
        comodel_name='school',
        ondelete='restrict',
    )

    # multimple roles can be filled by the same person 
    # (eg. Mr. Smith can both an English and a Math teacher at the same school)
    teacher_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete='restrict',
        domain=[('is_teacher','=',True)]
    )

    # link to the universal course name
    course_id = fields.Many2one(
        comodel_name='school.courses',
        ondelete='restrict',
    )


    @api.depends('teacher_id', 'course_id')
    def _compute_display_name(self):
        for record in self:
            combined_name = f"{record.course_id.name} by {record.teacher_id.name}"
            record.display_name = 'New' if 'False' in combined_name else combined_name
    
    def name_get(self):
        res = []
        for record in self:
            if record.course_id and record.teacher_id:
                res.append((record.id, f"{record.course_id.name} by {record.teacher_id.name}"))
            else:
                res += super(SchoolCoursesTeachers, record).name_get()
        return res