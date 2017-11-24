# -*- coding: utf-8 -*-

from odoo import models, fields, api
from rddata import *

class client(models.Model):
    _name = 'tech_directory.client'
    _rec_name = 'name'

    name = fields.Char(required = 'True')
    phone = fields.Text(required = 'True')
    client_code = fields.Text(required = 'True')
    E_mail = fields.Text(required = 'True')
    contact_person = fields.Text(required = 'True')
    independent_client = fields.Boolean()
    manager_ids = fields.Many2many("tech_directory.manager")
    manager_gk = fields.Many2many("res.users")
    contractor_ids = fields.One2many("tech_directory.contractor","client_id")
    client_my_button_fill  = fields.Boolean()

    @api.multi
    @api.onchange("client_my_button_fill")
    def _onchange_field(self):
        d=rdfast()
        for re in self:
            if re.client_my_button_fill:
                re.client_code = rdnums(3)+'-'+rdnums(2)
                re.name = d['name']
                re.phone = d['phone']
                re.E_mail = d['email']
                re.contact_person = d['fio']
                re.client_my_button_fill = False
