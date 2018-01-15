# -*- coding: utf-8 -*-

from odoo import models, fields, api
from rddata import *


class task(models.Model):
    _name = 'my_docs.task'
    _rec_name = 'name'
    _inherit = ['mail.thread']
    type_mail = fields.Selection(selection=[(
        'in', 'in'), ('out', 'out')], string="Tip task in or out", required=True)
    sender = fields.Char()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('new', 'New'),
        ('await_expert', 'await_expert'),
        ('await_client', 'await_client'),
        ('end', 'End')
    ])

    active = fields.Boolean(string="Field name", default=True)
    expert_enter = fields.Boolean(string="expert_enter", default=False)
    client_enter = fields.Boolean(string="client_enter", default=False)

    ApplicantType = fields.Selection(selection=[
        ('Manufacturer', u'Изготовитель'),
        ('Seller', u'Продавец'),
        ('Supplier', u'Поставщик'),
        ('AuthorizedPerson', u'Уполномоченное изготовителем лицо'),
    ], default="AuthorizedPerson")

    Applicant_partner_id = fields.Many2one(
        string="Field name",
        comodel_name="my_docs.partner"
    )
    Manufacturer_partner_id = fields.Many2one(
        string="Field name",
        comodel_name="my_docs.partner"
    )
    @api.onchange("Applicant_partner_id")
    @api.multi
    def _ApplicantInfo(self):
        for r in self:
            if self.Applicant_partner_id:
                self.ApplicantInfo = self.Applicant_partner_id.rek_result



    @api.onchange("Manufacturer_partner_id")
    @api.multi
    def _ManufacturerInfo(self):
        for r in self:
            if self.Manufacturer_partner_id:
                self.ManufacturerInfo = self.Manufacturer_partner_id.rek_result

    ApplicantInfo = fields.Text(compare=_ApplicantInfo)
    ManufacturerInfo= fields.Text(compare=_ManufacturerInfo)

    ProductType = fields.Selection(
        selection=[('Serial', 'Serial'), ('Part', 'Part'), ('Single', 'Single')])
    ProductInfo = fields.Text()
    ProductIdentification = fields.Text()
    ShippingDocumentation = fields.Char(
        string="Rekvizity tovarosoprovoditel'noj dokumentacii")
    Part = fields.Char(string="Kolichestvo partii")
    Invoice = fields.Char(string="Invoice")
    DeliveryContract = fields.Char(
        string="Nomer i data dogovora ili kontrakta o postavke produkcii")
    ProductIdentificationOther = fields.Char(
        string="Inaya informaciya, identificiruyushchaya produkciyu")

    tnved_ids = fields.Many2many(comodel_name="my_docs.tnved")
    reglament_ids = fields.Many2many("my_docs.reglament")

    DocumentValidity = fields.Char(
        string="Srok dejstviya deklaracii o sootvetstvii:")
    # AdditionalInfo
    AcceptanceReason = fields.Char(string="Protokol ispitanii")
    ProductLocation = fields.Selection(
        selection=[('Local', 'importnaya'), ('Foreign', 'otechestvennaya')])

    shema_id = fields.Many2one(
        comodel_name="my_docs.schema",
    )
    name = fields.Char()

    @api.one
    def toggle_client_enter(self):
        self.client_enter = not self.client_enter

    @api.one
    def toggle_expert_enter(self):
        self.expert_enter = not self.expert_enter

    @api.multi
    def state_draft(self):
        self.state = 'draft'
        self.log_prod(self.state)

    @api.multi
    def state_new(self):
        self.state = 'new'
        self.log_prod(self.state)

    @api.multi
    def state_await_expert(self):
        self.state = 'await_expert'
        self.log_prod(self.state)

    @api.multi
    def state_await_client(self):
        self.state = 'await_client'
        self.log_prod(self.state)

    @api.multi
    def state_end(self):
        self.state = 'end'
        self.log_prod(self.state)

    def log_prod(self, action):
        msg = str(action)
        return self.message_post(body=msg, message_type='comment')


class schema(models.Model):
    _name = 'my_docs.schema'
    name = fields.Char()
    doc_type = fields.Selection(selection=[('ds', 'ds'),
    ('ss', 'ss')])
