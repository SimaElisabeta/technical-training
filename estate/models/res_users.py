from odoo import fields, models


class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        comodel_name='estate_property',
        inverse_name='seller_id',
        domain=[('state', 'not in', [('sold', 'canceled')])]
    )
    