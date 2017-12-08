# -*- coding: utf-8 -*-

from odoo import models, fields, api
from rddata import *

class task(models.Model):
    _name = 'my_docs.task'
    _rec_name = 'name'
    type_mail=fields.Selection(selection=[('in', 'in'),('out', 'out')],string="Tip task in or out", required = True)
    sender = fields.Char()
    state = fields.Selection([
    ('draft', 'Draft'),
    ('new', 'New'),
    ('await_expert', 'await_expert'),
    ('await_client', 'await_client'),
    ('end', 'End')
    ])

    active =  fields.Boolean(string="Field name",default = True )
    expert_enter =  fields.Boolean(string="expert_enter", default = False )
    client_enter =  fields.Boolean(string="client_enter", default = False )

    def toggle_client_enter(self):
        self.client_enter = not self.client_enter

    applicant = fields.Char()
    ProductType= fields.Selection(selection=[('Serial', 'Serial'),('Part', 'Part'),('Single', 'Single')])
    ProductInfo= fields.Text()
    ProductIdentification = fields.Text()
    ShippingDocumentation = fields.Char(string="Rekvizity tovarosoprovoditel'noj dokumentacii")
    Part= fields.Char(string="Kolichestvo partii")
    Invoice= fields.Char(string="Invoice")
    DeliveryContract= fields.Char(string="Nomer i data dogovora ili kontrakta o postavke produkcii")
    ProductIdentificationOther= fields.Char(string="Inaya informaciya, identificiruyushchaya produkciyu")

    tnved_ids = fields.Many2many(comodel_name="my_docs.tnved")
    reglament_ids= fields.Many2many("my_docs.reglament")

    DocumentValidity = fields.Char(string="Srok dejstviya deklaracii o sootvetstvii:")
    # AdditionalInfo
    AcceptanceReason = fields.Char(string="Protokol ispitanii")
    shema = fields.Selection(selection=[('value1', 'description1'),('value2', 'description2')])
    name = fields.Char()

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_new(self):
        self.state = 'new'

    @api.multi
    def action_await_expert(self):
        self.state = 'await_expert'

    @api.multi
    def action_await_client(self):
        self.state = 'await_client'

    @api.multi
    def action_end(self):
        self.state = 'end'
