# -*- coding:utf-8 -*-
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _name = "purchase.order.line"
    _inherit = ['purchase.order.line']

    image_small = fields.Binary('Product Image', related='product_id.product_tmpl_id.image_small')


    item_number = fields.Integer('Item')

    @api.onchange('product_id')
    @api.multi
    def compute_qty(self):
        for rec in self:
            if rec.product_id:
                product = self.env['product.product'].search([('id', '=', rec.product_id.id)])
                rec.qty_available = product.qty_available

    qty_available = fields.Integer(string=u'Disponible', compute='compute_qty')

