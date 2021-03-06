from odoo import models, fields, api



class OrderLine(models.Model):
    _inherit = 'purchase.order.line'

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

    # account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account',
    #                                       domain=[('account_type', '=', 'normal')])

