# -*- coding: utf-8 -*-

from odoo import models, fields, api

class reglament(models.Model):
    _name = 'my_docs.reglament'

    name = fields.Text('Rglament name')
    number = fields.Char("Reglament number")
    group_id =  fields.Many2one(
        string="Group name")
