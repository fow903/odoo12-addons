# -*- coding:utf-8 -*-
from openerp import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    partner_ref = fields.Char()

    @api.multi
    @api.onchange('order_line')
    def _compute_item(self):
        print("Here")
        item = 0
        for line in self.order_line:
            item = item + 1
            line.item_number = item

    """@api.multi
    def button_process(self):
        self.write({'state': 'to approve'})
        return {}

    @api.multi
    def button_approve(self):
        self.write({'state': 'purchase'})
        self._create_picking()
        return {}

    @api.multi
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            if order.user_has_groups('purchase.group_doble_validacion'):
                order.write({'state': 'to approve'})
            else:
                order.write({'state': 'to approve'})
        return {}"""

    purchase_type_sel = [
        ('inventory_supply', 'Abastecimiento de Inventario'),
        ('administration_supply', 'Abastecimiento de Administración'),
        ('invoice', 'Factura'),
        ('sale_order', 'Pedido de venta'),
    ]
    purchase_type = fields.Selection(purchase_type_sel, string=u'Tipo de Compras', default=False)
    sale_order = fields.Many2one('sale.order', string='Documento')
    invoice = fields.Many2one('account.invoice', string='Documento')
