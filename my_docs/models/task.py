# -*- coding: utf-8 -*-

from odoo import models, fields, api
from rddata import *

class task(models.Model):
    _name = 'my_docs.task'
    _rec_name = 'name'
    _inherit = ['mail.thread']
    def generate_adress(self, record,vid_partner):
        print 'm0011111------------------------------------------'
        for r in record:
            res = []

            def _manufacturer_adress_generator():
                if not r.address_is_same and r.address != r.address_real:
                    if r.type_of_partner in ['urlico', 'fizlico', 'foreign']:
                        res.append(u'Место нахождения: ')
                    elif r.type_of_partner in ['ip']:
                        res.append(u'Место жительства: ')

                    if r.country_id.code == 'RU' : res.append(r.country_id.name)
                    if r.region_id:
                        res.append(r.region_id.name)
                    if r.index:
                        res.append(r.index)
                    if r.address:
                        res.append(r.address)
                    if r.country_id.code != 'RU' : res.append(r.country_id.name)

                    res.append(u'адрес места осуществления деятельности по изготовлению продукции: ')
                    if r.country_real_id.code == 'RU' : res.append(r.country_real_id.name)
                    if r.region_real_id:
                        res.append(r.region_real_id.name)
                    if r.index_real:
                        res.append(r.index_real)
                    if r.address_real:
                        res.append(r.address_real)
                    if r.country_real_id.code != 'RU' : res.append(r.country_real_id.name)

                else:
                    if r.type_of_partner in ['urlico', 'fizlico', 'foreign']:
                        res.append(
                            u'Место нахождения и адрес места осуществления деятельности по изготовлению продукции: ')
                    elif r.type_of_partner in ['ip']:
                        res.append(u'Место жительства и адрес места осуществления деятельности по изготовлению продукции: ')

                    if r.country_id.code == 'RU' : res.append(r.country_id.name)
                    if r.region_id:
                        res.append(r.region_id.name)
                    if r.index:
                        res.append(r.index)
                    if r.address:
                        res.append(r.address)
                    if r.country_id.code != 'RU' : res.append(r.country_id.name)

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
                        res.append(u'Место жительства и адрес места осуществления деятельности: '+ r.country_id.name)
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
            result = result.replace(': ,',': ')
            result = result.replace('  ',' ')
            return result

    @api.multi
    @api.onchange("ApplicantType")
    def _onchange_ApplicantType(self):
        print 'm00001------------------------------------------'
        if self.ApplicantType == "Manufacturer":
            self.Manufacturer_partner_id = self.Applicant_partner_id

    @api.multi
    @api.onchange("Applicant_partner_id","Manufacturer_partner_id")
    def _onchange_applicant(self):
        print 'm00002------------------------------------------'
        if self.Applicant_partner_id:
            self.ApplicantInfo = self.generate_adress(self.Applicant_partner_id,vid_partner='applicant')
            self.ApplicantInFace = self.Applicant_partner_id.fio_head_rod_pad + " " +  self.Applicant_partner_id.head_role_rod_pad

        if self.Manufacturer_partner_id:
            self.ManufacturerInfo = self.generate_adress(self.Manufacturer_partner_id,vid_partner='manufacturer')
            if self.Manufacturer_partner_id.country_id.code in ['RU','KZ','AR','BY','KY'] and self.Applicant_partner_id.country_id.code in ['RU','KZ','AR','BY','KY'] and self.Manufacturer_partner_id.country_id.code == self.Applicant_partner_id.country_id.code:
                self.ProductLocation = "Local"
            else:
                self.ProductLocation = "Foreign"

    @api.multi
    @api.onchange("task_my_button_fill")
    def _onchange_field(self):
        d = rdfast()
        for re in self:
            if re.task_my_button_fill:
                re.ProductInfo = d['production']

    type_task = fields.Selection(selection=[(
        'ss', 'ss'), ('ds', 'ds'), ('request', 'request')])


    expert_id = fields.Many2one(
        comodel_name="res.users"
    )

    getter_company_id = fields.Many2one(
        comodel_name="res.company"
    )
    sender_company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.user.company_id
    )


    state = fields.Selection([
        ('draft', 'Draft'),
        ('new', 'New'),
        ('await_expert', 'await_expert'),
        ('await_client', 'await_client'),
        ('end', 'End')
    ], default='draft')

    def open(self):
        print 'm0011111------------------------------------------'
        print self.id
    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """ Override read_group to always display all states. """
        if groupby and groupby[0] == "state":
            # Default result structure
            states = [
                ('draft', 'Draft'),
                ('new', 'New'),
                ('await_expert', 'await_expert'),
                ('await_client', 'await_client'),
                ('end', 'End')
            ]

            read_group_all_states = [{
                '__context': {'group_by': groupby[1:]},
                '__domain': domain + [('state', '=', state_value)],
                'state': state_value,
                'state_count': 0,
            } for state_value, state_name in states]
            # Get standard results
            read_group_res = super(task, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby)
            # Update standard results with default results
            result = []
            for state_value, state_name in states:
                res = filter(lambda x: x['state'] == state_value, read_group_res)
                if not res:
                    res = filter(lambda x: x['state'] == state_value, read_group_all_states)
                if state_value == 'cancel':
                    res[0]['__fold'] = True
                res[0]['state'] = [state_value, state_name]
                result.append(res[0])
            return result
        else:
            return super(task, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby)

    active = fields.Boolean( default=True)
    expert_enter = fields.Boolean(string="expert_enter", default=False)
    client_enter = fields.Boolean(string="client_enter", default=False)

    ApplicantType = fields.Selection(selection=[
        ('Manufacturer', u'Изготовитель'),
        ('Seller', u'Продавец'),
        ('Supplier', u'Поставщик'),
        ('AuthorizedPerson', u'Уполномоченное изготовителем лицо'),
    ], default="AuthorizedPerson")

    Applicant_partner_id = fields.Many2one(
        comodel_name="my_docs.partner_local"
    )

    Manufacturer_partner_id = fields.Many2one(
        comodel_name="my_docs.partner_local"
    )

    task_my_button_fill = fields.Boolean()

    ApplicantInfo = fields.Text()
    ApplicantInFace = fields.Char()
    ManufacturerInfo = fields.Text()

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

    tnved_ids = fields.Many2many(comodel_name="my_docs.tnved")
    reglament_ids = fields.Many2many("my_docs.reglament")

    DocumentValidity = fields.Char(
        string="Srok dejstviya deklaracii o sootvetstvii:")
    # AdditionalInfo
    AcceptanceReason = fields.Char(string="Protokol ispitanii")
    ProductLocation = fields.Selection(
        selection=[('Local', 'otechestvennaya'), ('Foreign', 'importnaya')], default="Local", readonly=True)

    shema_id = fields.Many2one(
        comodel_name="my_docs.schema",
    )
    name = fields.Char()

    @api.one
    def first_send(self):
        self.state = 'new'
        self.log_prod(self.state)

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
        return self.message_post(body=msg)




class company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'
    unic_id = fields.Char()
    friends_ids = fields.Many2many(

        comodel_name="my_docs.friends"
    )

class friend(models.Model):
    _name = 'my_docs.friends'

    def _domain(self):
        return [('id', '!=', self.env.user.company_id)]

    company_out_id = fields.Many2one(

        comodel_name="res.company"
    )
    name = fields.Char(related='company_out_id.name')
