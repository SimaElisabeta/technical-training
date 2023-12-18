from odoo import fields, models, api
from odoo import Command


class EstateProperty(models.Model):
    _inherit="estate_property"

    def set_state_sold(self):
        super().set_state_sold()

        for property in self:
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': property.buyer_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': 
                    [
                        Command.create({'name': property.name,'price_unit': property.selling_price * 0.06,'quantity': 1,}),
                        Command.create({'name': 'Administrative fees','price_unit': 100}),
                    ]
            }

            self.env['account.move'].create(invoice_vals)
