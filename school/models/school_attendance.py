from odoo import api, fields, models

class SchoolAttendance(models.Model):
    _name = "school.attendance"
    _description = "School Attendance"

    is_present = fields.Boolean()
    
    # add a text field named reason which is available if is_present is false
    
    date = fields.Date(
        default=fields.Date.context_today,
    )
    
    student_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete='restrict',
        domain=[('is_student','=',True)]
    )
    
    
    schedule_id = fields.Many2one(
        comodel_name='school.schedule',
        ondelete='restrict',
    )

    school_id = fields.Many2one(
        related="schedule_id.school_id",
        store=True
    )
    teacher_id = fields.Many2one(
        related="schedule_id.teacher_id",
        store=True
    )
    course_id = fields.Many2one(
       related="schedule_id.course_id",
        store=True
    )

    @api.onchange('student_id')
    def onchange_student_id(self):
        if self.student_id.school_id:
            return {'domain': {'schedule_id': [('school_id', '=', self.student_id.school_id.id)]}}