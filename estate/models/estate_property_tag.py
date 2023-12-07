from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    
    name = fields.Char(required=True, default="Unknown")
    color = fields.Integer()
    


###################################################### SQL constraints - field ######################################################
# _sql_constraints = [
#         ('check_', 'UNIQUE(name)', 'The tag name must be unique.')
#     ]