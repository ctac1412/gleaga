# -*- coding: utf-8 -*-

from odoo import models, fields, api

class doc_package(models.Model):
    _name = 'tech_directory.doc_package'

    name = fields.Char(required=True)
    type_komplekt = fields.Selection(
        string="type_komplekt",
        required=True,
        selection=[
                ('dogovor', 'dogovor'),
                ('dop_soglashenoie', 'dop soglashenoie'),
        ],
    )

    type_dogovora = fields.Selection(
        string="type_dogovora",
        required=True,
        selection=[
                ('predoplata', 'predoplata'),
                ('postoplata', 'postoplata'),
                ('other', 'other'),
        ],
    )
    prilojenia = fields.Char()
    comment = fields.Char()
    status = fields.Boolean(default=True)
