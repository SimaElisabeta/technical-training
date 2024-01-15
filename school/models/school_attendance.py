from odoo import api, fields, models
from odoo.exceptions import ValidationError

class SchoolAttendance(models.Model):
    _name = "school.attendance"
    _description = "School Attendance"
    _inherit = ['mail.thread']

    is_present = fields.Boolean()
    
    name = fields.Char(
        compute="_compute_name"
    )
    
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

    @api.depends('student_id', 'course_id', 'date')
    def _compute_name(self):
        for attendance in self:
            attendance.name = f"{attendance.student_id.name} attendance for {attendance.course_id.name}, on date {attendance.date}"

    @api.onchange('student_id')
    def onchange_student_id(self):
        if self.student_id.school_id:
            return {'domain': {'schedule_id': [('school_id', '=', self.student_id.school_id.id)]}}
        


    def notify_parent(self):
        for attendance in self:
            parent = attendance.student_id.parent_id
            if parent:
                msg = f"Your child absented the course {attendance.course_id.name} on date {attendance.date}"
                attendance.message_post(partner_ids=parent.ids, body=msg)
    


    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        not_present = res.filtered(lambda attendance: not attendance.is_present)
        not_present.notify_parent()
        return res
    

    def write(self, vals):
        for attendance in self:
            attendance._check_attendance_updates(attendance.date)
        res = super().write(vals)
        if "is_present" in vals and not vals["is_present"]:
            self.notify_parent()
        return res
    

    @api.model
    def _get_attendance_editing_deadline(self):
        # Get the deadline date from configuration settings
        deadline_date = self.env['ir.config_parameter'].sudo().get_param('school.interval_date_to_update_attendance')
        return fields.Date.to_date(deadline_date)

    @api.constrains('date')
    def _check_attendance_editing_deadline(self):
        for attendance in self:
            attendance._check_attendance_updates(attendance.date)
           
    def _check_attendance_updates(self, check_date):
        self.ensure_one()
        deadline_date = self._get_attendance_editing_deadline()
        if check_date and check_date <= deadline_date:
            raise ValidationError("You cannot edit or create attendance before the deadline date %s." % deadline_date)