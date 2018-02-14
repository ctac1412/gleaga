# -*- coding: utf-8 -*-

from odoo import models, fields, api
from rddata import *
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from yandex_translate import YandexTranslate
import datetime
translate = YandexTranslate('trnsl.1.1.20180202T132838Z.3c46e5ba934244c9.05623678a54abc23648ca4cee81697c5d46be3d0')

class local_task_kz(models.Model):
    _name = 'my_docs.local_task_kz'
    _inherit = ['my_docs.task']
    local_task_id = fields.Many2one('my_docs.local_task_kz')
    @api.multi
    @api.onchange("ProductInfo","ProductIdentification" )
    def _onchange_ProductInfo_kz(self):
        for r in self:
            if r.ProductInfo : r.ProductInfo_kz = translate.translate(r.ProductInfo, 'ru-kk')['text'][0]
            if r.ProductIdentification :r.ProductIdentification_kz  = translate.translate(r.ProductIdentification, 'ru-kk')['text'][0]

    @api.multi
    def write(self, vals={}):
        print 'm0099999999------------------------------------------'
        super(local_task_kz, self).write(vals)
        return True

    def qqqqqqqqqqqqqqqq(self):
        for r in self:
            print r
            # if r.ProductInfo : r.ProductInfo_kz = translate.translate(r.ProductInfo, 'ru-kk')['text']
            # if r.ProductIdentification :r.ProductIdentification_kz  = translate.translate(r.ProductIdentification, 'ru-kk')['text']
        # print('Languages:', translate.langs)
        # print('Translate directions:', translate.directions)
        # print('Detect language:', translate.detect('Привет, мир!'))

    ApplicantType_kz = fields.Selection(selection=[
        ('Manufacturer', u'Изготовитель'),
        ('Seller', u'Продавец'),
        ('Supplier', u'Поставщик'),
        ('AuthorizedPerson', u'Уполномоченное изготовителем лицо'),
    ], default="AuthorizedPerson")
    Applicant_partner_id_kz = fields.Many2one(
        comodel_name="my_docs.partner_local"
    )
    Manufacturer_partner_id_kz = fields.Many2one(
        comodel_name="my_docs.partner_local"
    )

    ApplicantInfo_kz = fields.Text()
    ApplicantInFace_kz = fields.Char()
    ManufacturerInfo_kz = fields.Text()
    ProductType_kz = fields.Selection(
        selection=[('Serial', u'Сериялық шығару'), ('Part', u'Партиялық шығару'), ('Single', u'бірлік шығару')], default="Serial",readonly=True)
    ProductInfo_kz = fields.Text()
    ProductIdentification_kz = fields.Text()
    ShippingDocumentation_kz = fields.Char(
        string="Rekvizity tovarosoprovoditel'noj dokumentacii")
    Part_kz = fields.Char(string="Kolichestvo partii")
    Invoice_kz = fields.Char(string="Invoice")
    DeliveryContract_kz = fields.Char(
        string="Nomer i data dogovora ili kontrakta o postavke produkcii")
    ProductIdentificationOther_kz = fields.Char(
        string="Inaya informaciya, identificiruyushchaya produkciyu")
    DocumentValidity_kz = fields.Char(
        string="Srok dejstviya deklaracii o sootvetstvii:")
    AcceptanceReason_kz = fields.Char(string="Protokol ispitanii")
    ProductLocation_kz = fields.Selection(
        selection=[('Local', 'otechestvennaya'), ('Foreign', 'importnaya')], default="Local", readonly=True)
    task_log_ids= fields.One2many(
        comodel_name="my_docs.task_log",
        inverse_name="task_id",
    )

    @api.onchange("ProductType")
    @api.multi
    def _onchange_ProductType_kz(self):
        for r in self:
            r.ProductType_kz=r.ProductType
            if r.ProductType == 'Serial':
                r.Part_kz= ''
                r.Invoice_kz= ''
