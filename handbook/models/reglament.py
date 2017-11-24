# -*- coding: utf-8 -*-

from odoo import models, fields, api

class reglament(models.Model):
    _name = 'tech_directory.reglament'

    name = fields.Text('Rglament name')
    number = fields.Char("Reglament number")
    status = fields.Boolean("Reglament status")
    group_id =  fields.Many2one(
        comodel_name="tech_directory.grouplist",
        string="Group name")
        
