# -*- coding: utf-8 -*-
{
    'name': "Validacion y Cantidades Compras",
    'summary': 'Cantidades y doble validacion',

    'description': """
        Cambios y Ajustes  en  Compras:
        Se agregaron en linea de orden imagen y numero de item
        hacer que compra tenga una doble validacion.
    """,

    'author': "Joel Payan",
    'category': 'Purchase Management',
    'version': '0.1',
    'depends': ['purchase'],

    'data': [
        'views/purchase_order_view.xml',
        #'views/report_purchaseorder.xml',
    ],

    "installable": True,
}
