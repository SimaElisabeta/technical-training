from odoo import fields, models, api
import logging

class EstateProperty(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]
    
    name = fields.Char(required=True, default="Unknown")
    sequence = fields.Integer(name='Sequence', default=1)

    property_ids = fields.One2many(
        comodel_name='estate_property',
        inverse_name='property_type_id',
    )

    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_type_id',
    )
    
    offer_count = fields.Integer(
        compute = "_compute_offer_count",
        string="Offers"
    )


    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(self.offer_ids)


    def action_view_all_property_type_offers(self):
        return {
            'name': 'Property Offers',
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',            
            'context': {'create': False},
            'domain': [('property_type_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }
