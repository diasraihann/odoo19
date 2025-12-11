import uuid
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LogisticShipment(models.Model):
    _name = 'logistic.shipment'
    _description = 'Shipment'
    _rec_name = 'shipment_id'
    

    # Shipment ID yang di-generate otomatis menggunakan UUID
    shipment_id = fields.Char(
        string='Shipment ID',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: str(uuid.uuid4())
    )
    
    name = fields.Selection([
        ('shopee', 'Shopee'),
        ('tokopedia', 'Tokopedia'),
        ('lazada', 'Lazada'),
        ('zalora', 'Zalora'),
        ('blibli', 'Blibli'),
        ('c2c', 'C2C'),
        ('b2b', 'B2B'),
        ('non_commercial', 'Non Commercial')
    ], string='Channel', required=True)
    
    service_type = fields.Selection([
        ('regular', 'Regular'),
        ('express', 'Express'),
        ('cargo', 'Cargo')
    ], string='Service Type', required=True, default='regular')
    
    sender = fields.Char(string='Sender', required=True)
    receiver = fields.Char(string='Receiver', required=True)
    weight = fields.Float(string='Weight (kg)', required=True)
    description = fields.Text(string='Shipment Description', required=True)
    due_date = fields.Date(string='Due Date', readonly=True, store=True, compute='_compute_due_date')
    
    update_date = fields.Datetime(
        string='Last Update',
        compute='_compute_update_date',
        store=True,
        readonly=True
    )

    # Relasi ke Shipment Tracking
    tracking_id = fields.One2many(
        comodel_name='shipment.tracking',
        inverse_name='shipment_id',
        string='Tracking'
    )

    # Status diambil dari last tracking (READONLY karena computed)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered')
    ], string='Status', compute='_compute_status', store=True, readonly=True)

    @api.depends('service_type')
    def _compute_due_date(self):
        """Hitung due_date berdasarkan service_type"""
        for record in self:
            if record.service_type:
                today = fields.Date.today()
                
                if record.service_type == 'regular':
                    record.due_date = today + timedelta(days=3)
                elif record.service_type == 'express':
                    record.due_date = today + timedelta(days=1)
                elif record.service_type == 'cargo':
                    record.due_date = today + timedelta(days=7)
                else:
                    record.due_date = today + timedelta(days=3)  # default
            else:
                record.due_date = False

    # CONSTRAINTS
    @api.constrains('weight')
    def _check_weight(self):
        """Validasi weight harus lebih dari 0.01 kg"""
        for record in self:
            if record.weight <= 0.01:
                raise ValidationError(
                    'Weight must be greater than 0.01 kg. '
                    'Current weight: %.2f kg' % record.weight
                )

    @api.constrains('sender', 'receiver')
    def _check_sender_receiver(self):
        """Validasi sender dan receiver tidak boleh sama"""
        for record in self:
            if record.sender and record.receiver:
                # Case-insensitive comparison dan trim whitespace
                sender_clean = record.sender.strip().lower()
                receiver_clean = record.receiver.strip().lower()
                
                if sender_clean == receiver_clean:
                    raise ValidationError(
                        'Sender and Receiver cannot be the same person!\n'
                        'Sender: %s\n'
                        'Receiver: %s' % (record.sender, record.receiver)
                    )

    @api.constrains('name', 'service_type', 'sender', 'receiver', 'weight', 'description')
    def _check_required_fields(self):
        """Validasi semua field required harus diisi (kecuali due_date yang auto-computed)"""
        for record in self:
            errors = []
            
            if not record.name:
                errors.append('Channel must be selected')
            
            if not record.service_type:
                errors.append('Service Type must be selected')
            
            if not record.sender:
                errors.append('Sender must be filled')
            
            if not record.receiver:
                errors.append('Receiver must be filled')
            
            if not record.weight:
                errors.append('Weight must be filled')
            
            if not record.description:
                errors.append('Shipment Description must be filled')
            
            if errors:
                raise ValidationError(
                    'Please complete the following required fields:\n\n' + 
                    '\n'.join(['• ' + error for error in errors])
                )

    @api.depends('tracking_id.status', 'tracking_id.timestamp')
    def _compute_status(self):
        status_map = {
            'drop_off': 'draft',
            'in_transit': 'in_transit',
            'arrived_dc': 'in_transit',
            'out_for_delivery': 'in_transit',
            'delivered': 'delivered'
        }
        for shipment in self:
            if shipment.tracking_id:
                latest_tracking = shipment.tracking_id.sorted(key='timestamp', reverse=True)[0]
                shipment.status = status_map.get(latest_tracking.status, 'draft')
            else:
                shipment.status = 'draft'
    
    def _update_status_from_tracking(self):
        """Method untuk trigger update status dari tracking"""
        self._compute_status()


    @api.depends('tracking_id.timestamp')
    def _compute_update_date(self):
        """Ambil timestamp dari tracking terakhir"""
        for shipment in self:
            if shipment.tracking_id:
                latest_tracking = shipment.tracking_id.sorted(key='timestamp', reverse=True)[0]
                shipment.update_date = latest_tracking.timestamp
            else:
                shipment.update_date = False

    def name_get(self):
        """Override name_get untuk menampilkan shipment_id di dropdown"""
        result = []
        for record in self:
            name = record.shipment_id or 'New'
            result.append((record.id, name))
        return result
    
    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """Override search untuk pencarian berdasarkan shipment_id"""
        args = args or []
        if name:
            args = args + [('shipment_id', operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)