from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
import logging

# logging.info("This is a message for the console.")

GARDEN_ORIENTATION_SELECTION = [
    ('north', 'North'),
    ('south', 'South'),
    ('east', 'East'),
    ('west', 'West'),
]

STATE_SELECTION = [
    ('new', 'New'),
    ('offer received', 'Offer Received'),
    ('offer accepted', 'Offer Accepted'),
    ('sold', 'Sold'),
    ('canceled', 'Canceled')
]


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property App"
    _order = "id desc"


    ###################################################### GENERAL functions ######################################################
    def _default_date_availability(self):
        default_date = fields.Date.today() + relativedelta(months=3)
        return default_date
    

    def _get_accepted_offer(self):
        for offer in self.offer_ids:
            if offer.status == 'accepted':
                return offer
    
    
    ###################################################### ESTATE PROPERTY - fields ######################################################
    name = fields.Char(required=True, default="Unknown", string = "Title")
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=_default_date_availability, string="Available From")
    expected_price = fields.Float(required=True)
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    living_area = fields.Integer(string = "Living Area (sqm)")
    garden_area = fields.Integer(string = "Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection = GARDEN_ORIENTATION_SELECTION,
        help = 'Select the orientation of the garden',
    )
    active = fields.Boolean(default = True) # when active = fields.Boolean() -> if default is not specified the value will always be: default = False
    
    state = fields.Selection(
        string='Status',
        required=True,
        default="new",
        selection=STATE_SELECTION,
        compute = '_compute_state',
        store=True
    )

    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        ondelete='restrict',
        required=True,
    )

    seller_id = fields.Many2one(
        default=lambda self: self.env.user,
        string='Salesman',
        comodel_name='res.users',
        ondelete='restrict',
    )

    buyer_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete='restrict',
        copy=False,
        compute = "_compute_buyer_id",
    )

    selling_price = fields.Float(
        readonly=True,
        copy=False,
        compute = "_compute_selling_price",
        store=True          # store=False -> this was the value before implementing _validate_selling_price
        )
    
    tag_ids = fields.Many2many(
        comodel_name='estate.property.tag',
    )
    
    offer_ids = fields.One2many(
        string='All Offers',
        comodel_name='estate.property.offer',
        inverse_name='estate_property_id',
    )

    total_area = fields.Integer(
        string = 'Total area (sqm)',
        compute = "_compute_total_area"
    )
    
    best_price = fields.Float(
        string='Best Offer',
        compute = "_compute_best_price"
    )
    
    ###################################################### ONCHANGE functions ######################################################
    '''
    ONCHANGE -> garden
    '''
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0    
            self.garden_orientation = None    
    

    ###################################################### COMPUTE functions ######################################################
    '''
    COMPUTE -> total_area
    '''
    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for property_record in self:
            property_record.total_area = property_record.garden_area + property_record.living_area


    '''
    COMPUTE -> best_price
    '''
    @api.depends("offer_ids")
    def _compute_best_price(self):
        prices = self.offer_ids.mapped('price')
        max_price = 0 if len(prices) == 0 else max(prices)
        self.best_price = max_price


    '''
    COMPUTE -> buyer_id
    '''
    @api.depends("offer_ids")
    def _compute_buyer_id(self):
        # set default buyer_id
        self.buyer_id = None

        for property_record in self:   
            accepted_offer = property_record._get_accepted_offer()        

            if accepted_offer:
                property_record.buyer_id = accepted_offer.partner_id


    '''
    COMPUTE -> selling_price
    '''
    @api.depends("offer_ids.status")
    def _compute_selling_price(self):
        self.selling_price = 0

        for property_record in self:  
            accepted_offer = property_record._get_accepted_offer()

            if accepted_offer:
                property_record.selling_price = accepted_offer.price


    '''
    COMPUTE -> state
    '''
    @api.depends("offer_ids.status")
    def _compute_state(self):
        for property_record in self:
            if property_record.state == 'canceled' or property_record.state == 'sold':
                continue

            # set the property_record.state to 'new' if there are no offers in current property_record
            if not property_record.offer_ids:   
                property_record.state = 'new'
            else:
                # if there are offers in offer_ids, iterate through the list of offers and get an accepted offer if found
                if self._get_accepted_offer():
                    # when one offer is found set the property_record to 'offer accepted' and return out of the _computed() function
                    property_record.state = 'offer accepted'
                    return True
                property_record.state = 'offer received'  

    
    def set_state_sold(self):
        for property_record in self:
            if property_record.state == 'sold':
                return True

            if property_record.state == 'canceled':
                raise UserError('Canceled properties cannot be sold')
            property_record.state = 'sold'
        
    def set_state_canceled(self):
        for property_record in self:
            if property_record.state == 'canceled':
                return True
            
            if property_record.state == 'sold':
                raise UserError('Sold properties cannot be canceled')
            property_record.state = 'canceled'
               


    ###################################################### PYTHON CONSTRAINS ######################################################
    @api.constrains('selling_price', 'expected_price')
    def _validate_selling_price(self):
        for property_record in self:
            for offer in self.offer_ids:
                if offer.status == 'accepted':
                    constrain_selling_price = property_record.expected_price * 0.9
                    if property_record.selling_price < constrain_selling_price:
                        raise ValidationError("Test selling price must be at least 90% of the expected price. You must reduce the expected price if you want to accept this offer.")

   


    ###################################################### SQL constraints - field ######################################################
    # _sql_constraints = [
    #         ('check_positive_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
    #         ('check_positive_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
    #     ]
