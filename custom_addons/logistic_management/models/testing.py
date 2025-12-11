from odoo import models, fields

class LogisticShipment(models.Model):
    _name = "logistic.shipment"
    _description = "Shipment"

    name = fields.Char(string="Shipment Name", required=True)
    sender = fields.Char(string="Sender")
    receiver = fields.Char(string="Receiver")
    weight = fields.Float(string="Weight (kg)")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered')
    ], string="Status", default='draft')
