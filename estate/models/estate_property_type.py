from odoo import fields, models, api
import logging

class EstateProperty(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"
    
    name = fields.Char(required=True, default="Unknown")
    sequence = fields.Integer(name='Sequence', default=1)

    property_ids = fields.One2many(
        comodel_name='estate_property',
        inverse_name='property_type_id',
    )

    




    # offer_ids = fields.One2many(
    #     comodel_name='estate.property.offer',
    #     inverse_name='property_type_id',
    # )
    
    
    # offer_count = fields.Integer(
    #     compute = "_compute_offer_count"
    # )


    # @api.depends("offer_ids")
    # def _compute_offer_count(self):
    #     for property in self.property_ids:

    #         self.offer_count = len()

    


###################################################### SQL constraints - field ######################################################
# _sql_constraints = [
#         ('check_', 'UNIQUE(name)', 'The property type name must be unique.')
#     ]

