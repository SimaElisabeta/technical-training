from odoo import models, fields
from odoo.exceptions import ValidationError
import logging



class SchoolAttendanceWizard(models.TransientModel):
    _name = 'school.attendance.wizard'
    _description = 'School Attendance Wizard'

    
    date = fields.Date(
        default=fields.Date.context_today,
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

    
    wizard_line_ids = fields.One2many(
        comodel_name='school.attendance.wizard.lines',
        inverse_name='wizard_id',
    )



    def action_create_lines(self):
        self.ensure_one()
        new_lines = []
        if self.schedule_id:
            logging.info("Created lines of Students")
            for student in self.schedule_id.class_id.student_ids:
                new_lines.append({
                    'wizard_id': self.id,
                    'student_id': student.id,
                    'is_present': False,
                })
            self.env["school.attendance.wizard.lines"].create(new_lines)
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'school.attendance.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('school.school_attendance_wizard_view_form').id,
            'res_id': self.id,
            'target': 'new',
        }
    

    def action_clear_lines(self):
        self.ensure_one()
        if self.wizard_line_ids:
            self.wizard_line_ids.unlink()
            logging.warning("Cleared lines of Students")
        else:
            raise ValidationError("List of students is empty.")
 
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'school.attendance.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('school.school_attendance_wizard_view_form').id,
            'res_id': self.id,
            'target': 'new',
        }


    def action_register_attendance(self):
        self.ensure_one()
        if self.wizard_line_ids:
            for student_line in self.wizard_line_ids:
                self.env["school.attendance"].create({
                    'date': self.date,
                    'schedule_id': self.schedule_id.id,
                    'student_id': student_line.student_id.id,
                    'is_present': student_line.is_present,
                })
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        else:
            raise ValidationError("List of students is empty, please add some data.")
        
        

class SchoolAttendanceWizardLine(models.TransientModel):
    _name = 'school.attendance.wizard.lines'
    _description = 'School Attendance Wizard Line'
    
    
    wizard_id = fields.Many2one(
        comodel_name='school.attendance.wizard',
        ondelete='restrict',
    )

    student_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete='restrict',
        domain=[('is_student','=',True)],
        readonly=True 
    )

    is_present = fields.Boolean()