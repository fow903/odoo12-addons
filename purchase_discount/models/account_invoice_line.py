# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice"

    def _prepare_invoice_line_from_po_line(self, line):
        vals = super(AccountInvoiceLine, self)._prepare_invoice_line_from_po_line(
            line)
        vals['discount'] = line.discount
        return vals
