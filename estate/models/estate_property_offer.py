from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare
import logging

STATUS_SELECTION = [
    ('accepted', 'Accepted'),
    ('refused', 'Refused'),
]


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be strictly positive"),
    ]


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
    
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        related="estate_property_id.property_type_id"
    )

    validity = fields.Integer(
        string='Validity (days)',
        default= 7 
    )

    date_deadline = fields.Date(
        string='Deadline',
        compute = "_compute_date_deadline",
        inverse = "_inverse_date_deadline",
    )
    


    ######################################################### CRUD methods ########################################################
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("estate_property_id") and vals.get("price"):
                prop = self.env["estate_property"].browse(vals["estate_property_id"])
                # We check if the offer is higher than the existing offers
                if prop.offer_ids:
                    max_offer = max(prop.mapped("offer_ids.price"))
                    if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                        raise UserError("The offer must be higher than %.2f" % max_offer)
                if prop.state in ['sold', 'canceled']:
                    raise UserError("You cannot make an offer on a sold/canceled property")
                prop.state = "offer received"
        return super().create(vals_list)
    
    # @api.model_create_multi
    # def create(self, vals_line):
    #     current_property_id = vals_line[0]["estate_property_id"]
    #     current_property_state = self.env["estate_property"].browse(current_property_id).state
    #     best_price = self.env["estate_property"].browse(current_property_id).get_best_price()

    #     print(f'---------CURRENT PROPERTY STATE--------- ID:{current_property_id}, {current_property_state}')
    #     if current_property_state in ['sold', 'canceled']:
    #         raise UserError("You cannot make an offer on a sold/canceled property")

    #     if vals_line[0]["price"] <= best_price:
    #         raise UserError(f"The offer must be higher than: {best_price}")
        
    #     return super().create(vals_line)

    ###################################################### BUTTONS functions ######################################################
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
    