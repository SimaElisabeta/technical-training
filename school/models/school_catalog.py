from odoo import fields, models, api
from odoo.exceptions import ValidationError

class SchoolCatalog(models.Model):
    _name = "school.catalog"
    _description = "School Catalog"


    student_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete='restrict',
        domain=[('is_student','=',True)]
    )
    class_id = fields.Many2one(
       related="student_id.class_id",
        store=True
    )

    grade = fields.Float(
        group_operator="avg",
        digits=(16, 2),
        # digits='Product Price',
    )

    date = fields.Date(
        default=fields.Date.context_today,
    )

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
    
    


    @api.constrains("grade")
    def _check_grade(self):
        for record in self:
            if record.grade < 1 or record.grade > 10:
                raise ValidationError("Grade must be between 1-10")
            

    @api.onchange('student_id')
    def onchange_student_id(self):
        if self.student_id.school_id:
            return {'domain': {'school_course_teacher_id': [('school_id', '=', self.student_id.school_id.id)]}}
