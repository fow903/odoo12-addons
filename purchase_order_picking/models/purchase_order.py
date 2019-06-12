from odoo import models, fields



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    picking_type_id = fields.Many2one('stock.picking.type',default=lambda self: self.env["stock.picking.type"].search([("barcoed","=", "def")]).id)