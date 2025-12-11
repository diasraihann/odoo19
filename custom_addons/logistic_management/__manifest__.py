{
    'name': "Logistic Management",
    'summary': "Manage logistics operations",
    'description': """Module to manage shipments and logistics operations""",
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Logistics',
    'version': '0.1',
    'depends': ['base'], 
    'data': [
        'security/ir.model.access.csv',
        'views/logistic_shipment.xml',
        'views/shipment_tracking.xml',
    ],    
    'installable': True,
    'application': True,
}
