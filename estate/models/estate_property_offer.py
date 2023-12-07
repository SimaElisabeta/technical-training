from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
import logging

STATUS_SELECTION = [
    ('accepted', 'Accepted'),
    ('refused', 'Refused'),
]


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"


    ###################################################### ESTATE PROPERTY OFFER - fields ######################################################
    price = fields.Float()
    status = fields.Selection(copy=False, selection=STATUS_SELECTION)

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete='restrict',       
        required=True, 
    )

    estate_property_id = fields.Many2one(
        comodel_name='estate_property',
        ondelete='restrict',
        required=True, 
    )
    
    property_type_id = fields.Integer(related="estate_property_id.property_type_id")
       

    validity = fields.Integer(
        string='Validity (days)',
        default= 7 
    )

    date_deadline = fields.Date(
        string='Deadline',
        compute = "_compute_date_deadline",
        inverse = "_inverse_date_deadline",
    )
    
    
    


    ###################################################### GENERAL functions ######################################################
    def action_offer_accepted(self):
        for offer in self:
            # if the state of the property is property.state='offer received', make changes on the status of the current offer (offer.status = 'accepted')
            if offer.estate_property_id.state == 'offer received' or offer.estate_property_id.state == 'new':
                offer.status = 'accepted'
            # else raise an error and do not allow any changes to offer.status
             # (this will not allow changes for offer.status -> if the property state is either: SOLD or CANCELED!)
            else:
                raise UserError('Offers cannot be accepted at this time')
            
             
    def action_offer_refused(self):
        for offer in self:
            # if the state of the property is property.state='offer received' OR 'offer accepted', make changes on the status of the current offer (offer.status = 'accepted')
            if offer.estate_property_id.state == 'offer received' or self.estate_property_id.state == 'offer accepted' or offer.estate_property_id.state == 'new':
                offer.status = 'refused'
            # else raise an error and do not allow any changes to offer.status
            # (this will not allow changes for offer.status -> if the property state is either: SOLD or CANCELED!)
            else:
                raise UserError('Offers cannot be refused at this time')



    ###################################################### COMPUTE functions ######################################################
    '''
    COMPUTE -> date_deadline
    '''
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        # First: the value from date_deadline is set with the value from validity

        # Createing the date (as date-time value) to be set for date_deadline field
        # date_deadline value dependes on the value from validity
        for offer in self:
            delta = relativedelta(days=offer.validity)
            if offer.create_date:
                offer.date_deadline = offer.create_date + delta
            else:
                offer.date_deadline = fields.Date.today() + delta
    

    '''
    INVERSE -> date_deadline
    '''
    def _inverse_date_deadline(self):
        # Inverting the date into a number/int and set the validity with the new value
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.today()).days
    


    ###################################################### SQL constraints - field ######################################################
    # _sql_constraints = [
    #         ('check_positive_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    #     ]
    