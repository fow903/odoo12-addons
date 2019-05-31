# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#
#    Copyright (c) All rights reserved:
#        (c) 2015  Edwin de los santos
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public Li#    You should have received a copy of the GNU Affero General Public License
#    along with this program.If not, see http://www.gnu.org/licenses
#'views/view.xml'
###############################
from odoo import models, fields, api
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    shop_id= fields.Many2one('shop.config',string='Sucursal',required=True)