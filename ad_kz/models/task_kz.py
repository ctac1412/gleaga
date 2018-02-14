# -*- coding: utf-8 -*-

from odoo import models, fields, api
from rddata import *
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from yandex_translate import YandexTranslate
import datetime
import json
import requests

translate = YandexTranslate(
    'trnsl.1.1.20180202T132838Z.3c46e5ba934244c9.05623678a54abc23648ca4cee81697c5d46be3d0')


def b_t_s(item):
    return item or ''


class app_type(models.Model):
    _name = 'ad_kz.app_type'
    name = fields.Char()
    name_kz = fields.Char()


class reg_number(models.Model):
    _name = 'ad_kz.reg_number'
    name = fields.Char(index=True)


class app_number(models.Model):
    _name = 'ad_kz.app_number'
    name = fields.Char(index=True)


class expert_person(models.Model):
    _name = 'ad_kz.expert_person'
    name = fields.Char(related='user_id.name')
    user_id = fields.Many2one(
        comodel_name="res.users",
        required=True
    )
    reglament_ids = fields.Many2many("ad_kz.reglament")


class task_kz(models.Model):
    _name = 'ad_kz.task_kz'
    _inherit = ['mail.thread']

    def get_print_report_kz(self):
        print 'm00007------------------------------------------'

    def get_print_report(self):
        print 'm00008------------------------------------------'
    # def test(self):
    #     item_list = ["app_date",
    #                  "start_date",
    #                  "end_date",
    #                  "comment",
    #                  "ApplicantType",
    #                  "ApplicantType_kz",
    #                  "type_task",
    #                  "state",
    #                  "active",
    #                  "ApplicantName",
    #                  "ApplicantInfo",
    #                  "ApplicantInfo_kz",
    #                  "ApplicantInFace",
    #                  "ApplicantInFace_kz",
    #                  "ManufacturerName",
    #                  "ManufacturerInfo",
    #                  "ManufacturerInfo_kz",
    #                  "ProductType",
    #                  "ProductInfo",
    #                  "ProductIdentification",
    #                  "ShippingDocumentation",
    #                  "Part",
    #                  "Invoice",
    #                  "DeliveryContract",
    #                  "ProductIdentificationOther",
    #
    #                  "DocumentValidity",
    #                  "AcceptanceReason",
    #                  "ProductLocation",
    #                  "reglament_ids",
    #                  "shema_id",
    #
    #                  "name",
    #                  "ProductType_kz",
    #                  "ProductInfo_kz",
    #                  "ProductIdentification_kz",
    #                  "ShippingDocumentation_kz",
    #                  "Part_kz",
    #                  "Invoice_kz",
    #                  "DeliveryContract_kz",
    #                  "DocumentValidity_kz",
    #                  "AcceptanceReason_kz",
    #                  "ProductLocation_kz"]
    #     ret = {}
    #     fields = self.fields_get()
    #     for i in item_list:
    #         if i == 'ApplicantName' :
    #             ret[i] = self.Applicant_partner_id.title or ""
    #         elif i == 'ManufacturerName' :
    #             ret[i] = self.Manufacturer_partner_id.title or ""
    #         elif i == 'reglament_ids' :
    #             res=[]
    #             for reglament in self.reglament_ids:
    #                 res.append({'name':reglament.name})
    #             ret[i] =  res
    #         elif i == 'shema_id' :
    #             ret[i] = self.shema_id.name or ""
    #         else:
    #             ret[i] = getattr(self, i) or ""
    #     r = requests.post("https://api.reporting.cloud/v1/document/merge?templateName=Test.doc&test=true", data={'mergeData': [json.dumps(ret)]})
    #     # print(r.status_code, r.reason)
    #     # print(r.text)

    last_file = fields.Binary()

    app_date = fields.Date(readonly=True, index=True,
                           default=fields.Date.context_today)

    start_date = fields.Date(default=fields.Date.context_today)
    end_date = fields.Date(default=fields.Date.context_today)
    reg_number_id = fields.Many2one(
        comodel_name="ad_kz.reg_number"
    )
    app_number_id = fields.Many2one(
        comodel_name="ad_kz.app_number"
    )
    expert_person_ids = fields.Many2many(
        comodel_name="ad_kz.expert_person",
    )

    comment = fields.Text()

    @api.onchange("ApplicantType")
    def _onchange_ApplicantType(self):
        self.ApplicantType_kz = self.ApplicantType

    ApplicantType = fields.Selection(selection=[
        ('Manufacturer', u'Изготовитель'),
        ('Seller', u'Продавец'),
        ('Supplier', u'Поставщик'),
        ('AuthorizedPerson', u'Уполномоченное изготовителем лицо'),
    ], default="AuthorizedPerson")

    ApplicantType_kz = fields.Selection(selection=[
        ('Manufacturer', u'Изготовитель'),
        ('Seller', u'Продавец'),
        ('Supplier', u'Поставщик'),
        ('AuthorizedPerson', u'Уполномоченное изготовителем лицо'),
    ], default="AuthorizedPerson", readonly=True)

    type_task = fields.Selection(selection=[(
        'ss', 'ss'), ('ds', 'ds'), ('request', 'request')], default='ds')

    state = fields.Selection([
        ('maket', 'maket'),
        ('zaregistrirovan', 'zaregistrirovan'),
        ('upload', 'upload')
    ], default='maket')

    active = fields.Boolean(default=True)

    Applicant_partner_id = fields.Many2one(
        comodel_name="ad_kz.partner_local_kz"
    )

    Manufacturer_partner_id = fields.Many2one(
        comodel_name="ad_kz.partner_local_kz"
    )

    Applicant_partner_id_kz = fields.Char(
        related='Applicant_partner_id.title_kz', readonly=True
    )

    Manufacturer_partner_id_kz = fields.Char(
        related='Manufacturer_partner_id.title_kz', readonly=True
    )

    ApplicantInfo = fields.Text()
    ApplicantInfo_kz = fields.Text()

    ApplicantInFace = fields.Char(readonly=True,compute='_compute_face')
    ApplicantInFace_kz = fields.Char(readonly=True,compute='_compute_face')

    ManufacturerInfo = fields.Text()
    ManufacturerInfo_kz = fields.Text()

    ProductType = fields.Selection(
        selection=[('Serial', 'Serial'), ('Part', 'Part'), ('Single', 'Single')], default="Serial")

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

    tnved_ids = fields.Many2many(
        comodel_name="ad_kz.tnved", string='Kod TNVED')
    reglament_ids = fields.Many2many("ad_kz.reglament")

    DocumentValidity = fields.Char(
        string="Srok dejstviya deklaracii o sootvetstvii:")
    AcceptanceReason = fields.Char(string="Protokol ispitanii")
    ProductLocation = fields.Selection(
        selection=[('Local', 'otechestvennaya'), ('Foreign', 'importnaya')], default="Local", readonly=True)
    shema_id = fields.Many2one(
        comodel_name="ad_kz.schema",
    )
    name = fields.Char(default=u"Новая задача")

    # supplement_free_form_ids = fields.One2many(
    #     comodel_name=".supplement_free_form",
    #     inverse_name="task_id",
    # )

    ProductType_kz = fields.Selection(
        selection=[('Serial', u'Сериялық шығару'), ('Part', u'Партиялық шығару'), ('Single', u'бірлік шығару')], default="Serial", readonly=True)
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
    dop_svedeniya = fields.Text()
    dop_svedeniya_kz = fields.Text()

    # task_log_ids= fields.One2many(
    #     comodel_name=".task_log",
    #     inverse_name="task_id",
    # )

    @api.onchange("ProductType")
    @api.multi
    def _onchange_ProductType_kz(self):
        for r in self:
            r.ProductType_kz = r.ProductType
            if r.ProductType == 'Serial':
                r.Part_kz = ''
                r.Invoice_kz = ''

    def generate_adress(self, record, vid_partner):
        for r in record:
            res = []

            def _manufacturer_adress_generator():
                if not r.address_is_same and r.address != r.address_real:
                    if r.type_of_partner in ['urlico', 'fizlico', 'foreign']:
                        res.append(u'Место нахождения: ')
                    elif r.type_of_partner in ['ip']:
                        res.append(u'Место жительства: ')

                    if r.country_id.code == 'RU':
                        res.append(r.country_id.name)
                    if r.region_id:
                        res.append(r.region_id.name)
                    if r.index:
                        res.append(r.index)
                    if r.address:
                        res.append(r.address)
                    if r.country_id.code != 'RU':
                        res.append(r.country_id.name)
                    res.append(
                        u'адрес места осуществления деятельности по изготовлению продукции: ')
                    if r.country_real_id.code == 'RU':
                        res.append(r.country_real_id.name)
                    if r.region_real_id:
                        res.append(r.region_real_id.name)
                    if r.index_real:
                        res.append(r.index_real)
                    if r.address_real:
                        res.append(r.address_real)
                    if r.country_real_id.code != 'RU':
                        res.append(r.country_real_id.name)

                else:
                    if r.type_of_partner in ['urlico', 'fizlico', 'foreign']:
                        res.append(
                            u'Место нахождения и адрес места осуществления деятельности по изготовлению продукции: ')
                    elif r.type_of_partner in ['ip']:
                        res.append(
                            u'Место жительства и адрес места осуществления деятельности по изготовлению продукции: ')

                    if r.country_id.code == 'RU':
                        res.append(r.country_id.name)
                    if r.region_id:
                        res.append(r.region_id.name)
                    if r.index:
                        res.append(r.index)
                    if r.address:
                        res.append(r.address)
                    if r.country_id.code != 'RU':
                        res.append(r.country_id.name)

            def _ogrn_generator():
                if r.type_of_partner in ['urlico', 'fizlico', 'foreign']:
                    if r.country_id.code == 'KZ':
                        return u'бизнес-идентификационный номер: ' + r.ogrn
                    elif r.country_id.code in ['BY', 'AR']:
                        return u'учетный номер плательщика: ' + r.ogr
                    elif r.country_id.code == 'KY':
                        return u'идентификационный налоговый номер налогоплательщика: ' + r.ogrn
                    elif r.country_id.code == 'RU':
                        return u'основной государственный регистрационный номер: ' + r.ogrn
                    else:
                        return u'основной государственный регистрационный номер: ' + r.ogrn
                elif r.type_of_partner in ['ip']:
                    if r.country_id.code == 'KZ':
                        # индивидуальный Идентификационный Номер
                        return u'бизнес-идентификационный номер: ' + r.ogrn
                    elif r.country_id.code in ['BY']:
                        return u'свидетельство о государственной регистрации индивидуального предпринимателя: ' + r.ogrn
                    elif r.country_id.code in ['AR']:
                        return u'свидетельство о государственной регистрации: ' + r.ogrn
                    elif r.country_id.code == 'KY':
                        return u'свидетельство о государственной регистрации физического лица, занимающегося предпринимательской деятельностью: ' + r.ogrn
                    elif r.country_id.code == 'RU':
                        return u'основной государственный регистрационный номер: ' + r.ogrn
                    else:
                        return u'основной государственный регистрационный номер: ' + r.ogrn

            def _applicant_adress_generator():
                if not r.address_is_same and r.address != r.address_real:
                    if r.type_of_partner in ['urlico', 'fizlico', 'foreign']:
                        res.append(u'Место нахождения: ' + r.country_id.name)
                    elif r.type_of_partner in ['ip']:
                        res.append(u'Место жительства: ' + r.country_id.name)
                    if r.region_id:
                        res.append(r.region_id.name)
                    if r.index:
                        res.append(r.index)
                    if r.address:
                        res.append(r.address)
                    res.append(
                        u'адрес места осуществления деятельности:' + r.country_real_id.name)
                    if r.region_real_id:
                        res.append(r.region_real_id.name)
                    if r.index_real:
                        res.append(r.index_real)
                    if r.address_real:
                        res.append(r.address_real)
                else:
                    if r.type_of_partner in ['urlico', 'fizlico', 'foreign']:
                        res.append(
                            u'Место нахождения и адрес места осуществления деятельности: ' + r.country_id.name)
                    elif r.type_of_partner in ['ip']:
                        res.append(
                            u'Место жительства и адрес места осуществления деятельности: ' + r.country_id.name)
                    if r.region_id:
                        res.append(r.region_id.name)
                    if r.index:
                        res.append(r.index)
                    if r.address:
                        res.append(r.address)

            def _applicant_other_generator():
                if r.ogrn:
                    res.append(_ogrn_generator())
                if r.phone:
                    res.append(u'телефон: ' + r.phone)
                if r.email:
                    res.append(u'адрес электронной почты: ' + r.phone)
                if r.faxnum:
                    res.append(u'факс: ' + r.faxnum)

            if vid_partner in ['applicant']:
                _applicant_adress_generator()
                _applicant_other_generator()
            elif vid_partner in ['manufacturer']:
                _manufacturer_adress_generator()

            result = ", ".join(res)
            result = result.replace(': ,', ': ')
            result = result.replace('  ', ' ')
            return result

    @api.multi
    @api.onchange("Applicant_partner_id", "Manufacturer_partner_id")
    def _compute_face(self):
        for r in self:
            if r.Applicant_partner_id:
                if r.Applicant_partner_id.head_role_rod_pad and r.Applicant_partner_id.fio_head_rod_pad:
                    r.ApplicantInFace = r.Applicant_partner_id.head_role_rod_pad + " " + r.Applicant_partner_id.fio_head_rod_pad
                if r.Applicant_partner_id.head_role_rod_pad_kz and r.Applicant_partner_id.fio_head_rod_pad_kz:
                    r.ApplicantInFace_kz = r.Applicant_partner_id.head_role_rod_pad_kz + " " + r.Applicant_partner_id.fio_head_rod_pad_kz


    @api.multi
    @api.onchange("Applicant_partner_id", "Manufacturer_partner_id")
    def _onchange_applicant(self):
        for r in self:
            if r.Applicant_partner_id:
                r.ApplicantInfo = r.generate_adress(
                    r.Applicant_partner_id, vid_partner='applicant')

            if r.Manufacturer_partner_id:
                r.ManufacturerInfo = r.generate_adress(
                    r.Manufacturer_partner_id, vid_partner='manufacturer')
            # if self.Manufacturer_partner_id.country_id.code in ['RU', 'KZ', 'AR', 'BY', 'KY'] and self.Applicant_partner_id.country_id.code in ['RU', 'KZ', 'AR', 'BY', 'KY'] and self.Manufacturer_partner_id.country_id.code == self.Applicant_partner_id.country_id.code:
            #     self.ProductLocation = "Local"
            # else:
            #     self.ProductLocation = "Foreign"


class tnved(models.Model):
    _name = 'ad_kz.tnved'
    _rec_name = 'name'

    name = fields.Char('Code', size=256, required=True, index=True)
    note = fields.Text('Tnved Description', required=True, index=True)
    note_kz = fields.Text('Tnved Description KZ', required=True, index=True)


class schema(models.Model):
    _name = 'ad_kz.schema'
    name = fields.Char()
    doc_type = fields.Selection(selection=[('ds', 'ds'),
                                           ('ss', 'ss')])


class reglament(models.Model):
    _name = 'ad_kz.reglament'
    name = fields.Text('Rglament name')
    number = fields.Char("Reglament number")
    name_kz = fields.Text('Rglament name KZ')
    number_kz = fields.Char("Reglament number KZ")


class post(models.Model):
    _name = 'ad_kz.post'
    _rec_name = 'post_im_pad'

    @api.multi
    def name_get(self, context={}):
        for r in self:

            if r._context is None:
                context = {}
            if isinstance(r._ids, (int, long)):
                ids = [ids]
            res = []
            if r._context.get('special_display_name', False):
                for record in r.browse(r.id):
                    res.append((record.id, record.post_im_pad_kz))
            else:
                # Do a for and set here the standard display name, for example if the standard display name were name, you should do the next for
                for record in r.browse(r.id):
                    res.append((record.id, record.post_im_pad))
            return res

    post_im_pad = fields.Char()
    post_rd_pad = fields.Char()

    post_im_pad_kz = fields.Char()
    post_rd_pad_kz = fields.Char()


class country(models.Model):
    _name = 'ad_kz.country'
    name = fields.Char('Country Name', required=True, index=True)
    name_kz = fields.Char('Country Name KZ', required=True, index=True)
    code = fields.Char('Country Code', size=4, required=True, index=True)
    # def name_get(self,context={} ):
    #     if self._context is None:
    #         context = {}
    #     if isinstance(self._ids, (int, long)):
    #         ids = [ids]
    #     res = []
    #     if self._context.get('special_display_name', False):
    #         for record in self.browse(self.id):
    #             res.append((record.id,record.name))
    #     else:
    #         # Do a for and set here the standard display name, for example if the standard display name were name, you should do the next for
    #         for record in self.browse(self.id):
    #             res.append((record.id,record.name_kz))
    #     return res


class proove_form(models.Model):
    _name = 'ad_kz.proove_form'
    name = fields.Char('Proove Name', required=True, index=True)
    name_kz = fields.Char('Proove Name KZ', required=True)
    country_id = fields.Many2one(
        comodel_name="ad_kz.country"
    )


class fio_item(models.Model):
    _name = 'ad_kz.fio_item'
    # _rec_name = 'compute_name'
    name = fields.Char('FIO Rukovoditelya', index=True)
    name_rod_pad = fields.Char(
        'FIO Rukovoditelya v Roditelnom Padege', required=True)
    name_dat_pad = fields.Char('FIO Rukovoditelya v Datelnom padege')

    name_kz = fields.Char('FIO Rukovoditelya KZ', index=True)
    name_rod_pad_kz = fields.Char(
        'FIO Rukovoditelya v Roditelnom Padege KZ', required=True)
    name_dat_pad_kz = fields.Char('FIO Rukovoditelya v Datelnom padege KZ')

    post_id = fields.Many2one(
        comodel_name="ad_kz.post")

    @api.multi
    def _compute_name(self):
        for r in self:
            r.compute_name = b_t_s(
                r.post_id.post_im_pad_kz) + ' ' + b_t_s(r.name_kz)

    compute_name = fields.Char(compute=_compute_name)

    @api.multi
    def name_get(self, context={}):
        for r in self:

            if r._context is None:
                context = {}
            if isinstance(r._ids, (int, long)):
                ids = [ids]
            res = []
            if r._context.get('special_display_name', False):
                for record in r.browse(r.id):
                    name = b_t_s(record.post_id.post_im_pad_kz) + \
                        ' ' + b_t_s(record.name_kz)
                    res.append((record.id, name))
            else:
                # Do a for and set here the standard display name, for example if the standard display name were name, you should do the next for
                for record in r.browse(r.id):
                    name = b_t_s(record.post_id.post_im_pad) + \
                        ' ' + b_t_s(record.name)
                    res.append((record.id, name))
            return res
    # post_id_rod_pad = fields.Char(
    #     related="head_role.post_rd_pad", readonly=True)
    # post_id_kz = fields.Char(
    #     related="head_role.post_im_pad_kz", readonly=True
    # )
    # post_id_rod_pad_kz = fields.Char(
    #             related="head_role.post_rd_pad_kz", readonly=True)


class country_region(models.Model):
    _name = 'ad_kz.country_region'
    name = fields.Char('Region Name', required=True, index=True)
    name_kz = fields.Char('Region Name KZ', required=True)
    country_id = fields.Many2one(
        comodel_name="ad_kz.country"
    )


class type_ip(models.Model):
    _name = 'ad_kz.type_ip'
    name = fields.Char('Type_form', required=True)
