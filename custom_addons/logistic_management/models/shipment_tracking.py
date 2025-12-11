from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import uuid

class ShipmentTracking(models.Model):
    _name = 'shipment.tracking'
    _description = 'Shipment Tracking'
    _order = 'timestamp desc'

    tracking_id = fields.Char(
        string='Tracking ID',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: str(uuid.uuid4())
    )
    
    # Relasi ke Logistic Shipment
    shipment_id = fields.Many2one(
        'logistic.shipment',
        string='Shipment ID',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    timestamp = fields.Datetime(
        string='Timestamp',
        default=fields.Datetime.now,
        required=True,
        readonly=True
    )
    
    drop_point = fields.Char(
        string='Drop Point',
        required=True
    )
    
    location = fields.Char(
        string='Location',
        required=True
    )
    
    status = fields.Selection([
        ('drop_off', 'Dropped Off'),
        ('in_transit', 'In Transit'),
        ('arrived_dc', 'Arrived at DC'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered')
    ], string='Status', default='drop_off', required=True)
    
    note = fields.Text(string='Note')
    
    responsible = fields.Char(
        string='Responsible',
        required=True
    )

    @api.constrains('drop_point')
    def _check_drop_point(self):
        for record in self:
            if not record.drop_point or not record.drop_point.strip():
                raise ValidationError(_('Drop Point tidak boleh kosong!'))

    @api.constrains('location')
    def _check_location(self):
        for record in self:
            if not record.location or not record.location.strip():
                raise ValidationError(_('Location tidak boleh kosong!'))

    @api.constrains('responsible')
    def _check_responsible(self):
        for record in self:
            if not record.responsible or not record.responsible.strip():
                raise ValidationError(_('Responsible tidak boleh kosong!'))

    @api.constrains('shipment_id')
    def _check_shipment_id(self):
        for record in self:
            if not record.shipment_id:
                raise ValidationError(_('Shipment ID tidak boleh kosong!'))

    @api.model_create_multi
    def create(self, vals_list):
        trackings = super().create(vals_list)
        # Update status otomatis di shipment untuk setiap tracking yang dibuat
        for tracking in trackings:
            if tracking.shipment_id:
                tracking.shipment_id._update_status_from_tracking()
        return trackings
    
    def write(self, vals):
        result = super().write(vals)
        # Update status di shipment jika status tracking berubah
        if 'status' in vals:
            for tracking in self:
                if tracking.shipment_id:
                    tracking.shipment_id._update_status_from_tracking()
        return result
    
    def unlink(self):
        # Simpan shipment_id sebelum dihapus
        shipments = self.mapped('shipment_id')
        result = super().unlink()
        # Update status shipment setelah tracking dihapus
        for shipment in shipments:
            shipment._update_status_from_tracking()
        return result