# -*- coding: utf-8 -*-

from odoo import models, fields, api

class tnved(models.Model):
    _name = 'my_docs.tnved'

    name = fields.Text('name')
    text = fields.Char("text")
    parent_id =  fields.Char("parent_id")
