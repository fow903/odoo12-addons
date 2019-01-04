# -*- coding: utf-8 -*-
from odoo import api, fields, models, exceptions
import odoo.addons.decimal_precision as dp


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    account_analytic_id = fields.Many2one('account.analytic.account', string='Cuenta Analitica', domain=[('active', '=', True)])
    discount = fields.Float(
        string='Descuento (%)',digits_compute=dp.get_precision('Discount'))

    @api.depends('order_line.price_total')
    def _amount_all(self):
        orders = self.filtered(lambda x: (
            x.company_id.tax_calculation_rounding_method == 'round_globally'))
        orders._amount_all_round_globally()
        super(PurchaseOrder, self - orders)._amount_all()

    def _amount_all_round_globally(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.taxes_id.compute_all(
                    price, line.order_id.currency_id, line.product_qty,
                    product=line.product_id, partner=line.order_id.partner_id)
                amount_tax += sum(
                    t.get('amount', 0.0) for t in taxes.get('taxes', []))
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

    @api.depends('order_line.price_unit', 'order_line.taxes_id', 'order_line.product_qty',
                 'order_line.price_subtotal', 'order_line.amount_discount')
    def _compute_total_discount_grabado(self):

        for order in self:
            total_g = total_d = 0.0

            for line in order.order_line:

                if line.amount_discount > 0:
                    total_d += ((line.price_unit - line.amount_discount) * line.product_qty)

                if line.price_tax > 0:
                    total_g += line.price_subtotal

            order.update({
                'total_amount_discount': total_d,
                'total_grabado': total_g
            })

    total_amount_discount = fields.Float(compute='_compute_total_discount_grabado', string='Descuento', readonly=True,
                                         store=True)
    total_grabado = fields.Float(compute='_compute_total_discount_grabado', string='Grabado', readonly=True, store=True)


    @api.depends('order_line.price_total')
    def _amount_all(self):
        orders = self.filtered(lambda x: (
            x.company_id.tax_calculation_rounding_method == 'round_globally'))
        orders._amount_all_round_globally()
        super(PurchaseOrder, self - orders)._amount_all()

    def _amount_all_round_globally(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.taxes_id.compute_all(
                    price, line.order_id.currency_id, line.product_qty,
                    product=line.product_id, partner=line.order_id.partner_id)
                amount_tax += sum(
                    t.get('amount', 0.0) for t in taxes.get('taxes', []))
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"


    account_analytic_id = fields.Many2one('account.analytic.account',default=lambda self: self.env.context.get("account_analytic",None))

    @api.depends('discount')
    def _compute_amount(self):
        prices = {}
        for line in self:
            if line.discount:
                prices[line.id] = line.price_unit
                line.price_unit *= (1 - line.discount / 100.0)
            super(PurchaseOrderLine, line)._compute_amount()
            if line.discount:
                line.price_unit = prices[line.id]

    discount = fields.Float(
        string='Discount (%)',default=lambda self: self.env.context.get("discount",0), digits_compute=dp.get_precision('Discount'))

    _sql_constraints = [
        ('discount_limit', 'CHECK (discount <= 100.0)',
         'Discount must be lower than 100%.'),
    ]

    @api.multi
    def _get_stock_move_price_unit(self):
        """Get correct price with discount replacing current price_unit
        value before calling super and restoring it later for assuring
        maximum inheritability.
        """
        if self.discount:
            price_unit = self.price_unit
            self.price_unit *= (100 - self.discount) / 100
        price = super(PurchaseOrderLine, self)._get_stock_move_price_unit()
        if self.discount:
            self.price_unit = price_unit
        return price

    @api.depends('discount', 'price_unit')
    def _compute_amount_discount(self):

        for line in self:
            if line.discount > 0:
                total = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            else:
                total = line.price_unit
            line.update({
                'amount_discount': total
            })

    amount_discount = fields.Float(compute='_compute_amount_discount',default=lambda self: self.env.context.get('discount',0), string='Precio con Descuento', readonly=True,
                                   store=True)

    @api.one
    @api.constrains('discount')
    def constraints(self):
        if self.order_id.partner_id.category_id:
            if self.discount >= self.order_id.partner_id.category_id.max_discount:
                raise exceptions.ValidationError(
                    'A sobrepasado el limite de descuento de este cliente, el cual es un ' + str(
                        self.order_id.partner_id.category_id.max_discount) + "%")