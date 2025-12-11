# from odoo import http


# class LogisticManagement(http.Controller):
#     @http.route('/logistic_management/logistic_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/logistic_management/logistic_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('logistic_management.listing', {
#             'root': '/logistic_management/logistic_management',
#             'objects': http.request.env['logistic_management.logistic_management'].search([]),
#         })

#     @http.route('/logistic_management/logistic_management/objects/<model("logistic_management.logistic_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('logistic_management.object', {
#             'object': obj
#         })

