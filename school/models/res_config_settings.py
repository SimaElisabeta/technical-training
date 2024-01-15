# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    interval_date_to_update_attendance = fields.Datetime(
        string="Deadline for Updating Attendance",
        config_parameter='school.interval_date_to_update_attendance',
    )


