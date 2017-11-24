# -*- coding: utf-8 -*-

from odoo import models, fields, api
from rddata import *

class manager(models.Model):
    _name = 'tech_directory.manager'

    name = fields.Text()
    phone = fields.Text()
    E_mail = fields.Text()
    client_id = fields.Many2many("tech_directory.client",readonly=True)
    manager_fill  = fields.Boolean(store='False')

    @api.multi
    @api.onchange("manager_fill")
    def _onchange_field(self):
        d=rdfast()
        for re in self:
            if re.manager_fill:
                re.name = d['fio']
                re.phone = d['phone']
                re.E_mail = d['email']
                re.manager_fill=False
    
