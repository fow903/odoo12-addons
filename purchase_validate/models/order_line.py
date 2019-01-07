# -*- coding:utf-8 -*-
from openerp import models, fields, api


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

    @api.onchange('product_id')
    @api.multi
    def compute_qty_pro(self):
        for rec in self:
            if rec.product_id:
                product = self.env['product.product'].search([('id', '=', rec.product_id.id)])
                rec.immediately_usable_qty = product.immediately_usable_qty

    immediately_usable_qty = fields.Integer(string=u'Pronosticada', compute='compute_qty_pro')

    @api.onchange('product_id')
    @api.multi
    def compute_qty_potencial(self):
        for rec in self:
            if rec.product_id:
                product = self.env['product.product'].search([('id', '=', rec.product_id.id)])
                rec.potential_qty = product.potential_qty

    potential_qty = fields.Integer(string=u'Potencial', compute='compute_qty_potencial')

    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account',
                                          domain=[('account_type', '=', 'normal')])

