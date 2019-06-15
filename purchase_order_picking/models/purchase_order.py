from odoo import models, api, fields



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    picking_type_id = fields.Many2one('stock.picking.type')


